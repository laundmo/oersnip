from typing import List
from jinja2 import Environment as JinjaEnvironment, select_autoescape
from jinja2.loaders import FunctionLoader

from environments import envs
from pathlib import Path

from functools import partial
from itertools import chain

from yaml import load, dump
from rapidfuzz import process, fuzz

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

load = partial(load, Loader=Loader)
dump = partial(dump, Dumper=Dumper)

class EnvironmentNotFound(Exception):
    def __init__(self, environment=None, snippet_name=None):
        super().__init__(f"Missing environment '{environment}' for snippet '{snippet_name}'")

class Snippet:
    def __init__(
        self,
        name: str,
        jinjaenv: JinjaEnvironment,
        tags: List[str] = None,
        required_envs: List[str] = None,
    ):
        self.name = name
        self.template = jinjaenv.get_template(name)
        self.tags = tags or []
        self.required_envs = required_envs or []

    def resolve_environments(self):
        for environment in self.required_envs:
            if environment not in envs.keys():
                raise EnvironmentNotFound(environment=environment, snippet_name=self.name)
        return {
            key: value
            for _, env in envs.items()
            for key, value in env.environment().items()
        }

    def render(self):
        return self.template.render(**self.resolve_environments())

    @property
    def search_term(self):
        return " ".join([self.name, *self.tags])

class SnippetsSearch:
    snippet_path = Path("snippets")

    def __init__(self):
        self.snippets = {}  # TODO: make snippets hot-reloadable
        self.templates = {}
        def load_template(name):
            return self.templates[name]  # consider returning tuple with uptodatefunc
        self.env = JinjaEnvironment(
            loader=FunctionLoader(load_template), autoescape=select_autoescape()
        )
        self.load_all_snippets()

    def load_all_snippets(self):
        for file in chain(
            self.snippet_path.rglob("*.yaml"), self.snippet_path.rglob("*.yml")
        ):
            with file.open("r") as f:
                snippet = load(f)
            for key, snippet in snippet.items():
                self.templates[key] = snippet["template"]
                self.snippets[key] = Snippet(
                    key,
                    self.env,
                    tags=snippet["tags"],
                    required_envs=snippet["required_envs"],
                )

    def render_snippet(self, name):
        return self.snippets[name].render()

    def search_snippet(self, term):
        snippet_choice_pair = {
           s.search_term: s
           for s in self.snippets.values()
        }

        # Get ranked results by search term
        results = process.extract(term, snippet_choice_pair.keys(), scorer=fuzz.partial_token_sort_ratio, score_cutoff=20)
        
        # Get snippets instead of search term...
        results = [
            (snippet_choice_pair[r[0]], *r[1:])
            for r in results
        ]
        
        return results

if __name__ == "__main__":
    s = SnippetsSearch()
    print(s.search_snippet("test"))