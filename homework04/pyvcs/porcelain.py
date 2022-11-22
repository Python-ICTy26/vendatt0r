import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    res = commit_tree(gitdir, write_tree(gitdir, index), message, author)
    return res


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    head = gitdir / "refs" / "heads" / obj_name

    if head.exists():
        with head.open(mode="r") as f:
            obj_name = f.read()

    index = read_index(gitdir)

    for file in index:
        if pathlib.Path(file.name).is_file():
            if "/" in file.name:
                shutil.rmtree(file.name[: file.name.index("/")])
            else:
                os.remove(file.name)

    obj_path = gitdir / "objects" / obj_name[:2] / obj_name[2:]

    with obj_path.open(mode="rb") as f1:
        sha = commit_parse(f1.read()).decode()

    for file1 in find_tree_files(sha, gitdir):
        if "/" in file1[0]:
            dir_name = file1[0][: file1[0].find("/")]
            pathlib.Path(dir_name).absolute().mkdir()

        with open(file1[0], "w") as f2:
            header, content = read_object(file1[1], gitdir)
            f2.write(content.decode())
