from typing import Optional

from config import Settings


class GithubLogParser:
    def __init__(self, build_log: str, settings: Settings):
        self.build_log = build_log
        self.settings = settings

    def _find_position(self, string: str) -> Optional[int]:
        search_position = self.build_log.find(string)

        # skip all occurrences that start with a comma,
        # e.g. from source code like `echo "TASKID is ..."`,
        # which is echoed to the log before being executed
        while search_position > 0 and \
                (self.build_log[search_position - 1] == '"' or self.build_log[search_position - 1] == "'"):
            search_position = self.build_log.find(string, search_position + 1)

        if search_position < 0:
            return None

        search_position += len(string) + 1

        return search_position

    def parse_task_id(self) -> Optional[int]:
        task_id_position = self._find_position(self.settings.PREFIX_LOG_TASK_ID)
        if not task_id_position:
            return None

        try:
            return int(self.build_log[task_id_position:task_id_position + 2].strip())
        except ValueError:
            pass

        return None

    def parse_grading_points(self) -> Optional[float]:
        if (position := self._find_position(self.settings.PREFIX_LOG_SCORE)) is not None:
            return float(self.build_log[position:self.build_log.find("\n", position)].strip())
        if (position := self._find_position(self.settings.PREFIX_LOG_POINTS)) is not None:
            return float(self.build_log[position:self.build_log.find("/", position)].strip())
        return None

    def parse_grade_reduction_coefficient(self) -> Optional[str]:
        position = self._find_position(self.settings.PREFIX_LOG_REDUCTION)
        if position is None:
            return position
        reduction_percent = int(self.build_log[position:self.build_log.find("%", position)].strip())
        if not reduction_percent:
            return None
        else:
            return '{0:g}'.format(0.01 * (100 - reduction_percent))
