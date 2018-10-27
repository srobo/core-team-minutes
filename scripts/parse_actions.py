import re
import typing

Action = typing.NamedTuple('Action', (
    ('id', typing.Optional[int]),
    ('owner', str),
    ('title', str),
))

ACTION_POINT_REGEX = re.compile(r'[\s\*-]*(?P<owner>[-\w\s]+)( will|:) (?P<title>[^\.]+)')


def action_url(action_id: int) -> str:
    return 'https://github.com/srobo/core-team-minutes/issue/{}'.format(action_id)


def action_link(action_id: int) -> str:
    return "[#{}]({})".format(action_id, action_url(action_id))


def parse_actions(text: str) -> typing.Sequence[Action]:
    lines = text.splitlines()

    action_points_index = lines.index("## Action Points")

    actions = [] # type: typing.List[Action]

    for line in lines[action_points_index:]:
        match = ACTION_POINT_REGEX.search(line)
        if match is not None:
            actions.append(Action(
                id=None,
                owner=match.group('owner'),
                title=match.group('title'),
            ))

    return actions


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('minutes_file', type=argparse.FileType())
    args = parser.parse_args()

    for action in parse_actions(args.minutes_file.read()):
        print(action)
