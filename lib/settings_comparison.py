# -*- coding: utf-8 -*-
from typing import Dict
from prettytable import PrettyTable


class SettingsComparison:
    def __init__(self, db_result1, db_result2):
        self.db_results1 = db_result1
        self.db_results2 = db_result2
        self.different_settings = []

    @staticmethod
    def from_settings_tuple_to_dict(settings_tuple) -> Dict:
        settings_dict = {}
        for setting in settings_tuple:
            settings_dict[setting[0]] = setting[1]
        return settings_dict

    def _find_different_pg_settings(self):
        settings_dict1 = self.from_settings_tuple_to_dict(self.db_results1.result)
        settings_dict2 = self.from_settings_tuple_to_dict(self.db_results2.result)

        for setting_name, setting_value in settings_dict1.items():
            if settings_dict2.get(setting_name, None) is None:
                self.different_settings.append([setting_name, setting_value, None])
            else:
                if settings_dict2[setting_name] != setting_value:
                    self.different_settings.append(
                        [setting_name, setting_value, settings_dict2[setting_name]]
                    )

        for setting_name, setting_value in settings_dict2.items():
            if settings_dict1.get(setting_name, None) is None:
                self.different_settings.append([setting_name, None, setting_value])

    def show_different_settings(self) -> None:
        self._find_different_pg_settings()
        table = PrettyTable()
        table.field_names = [
            "setting",
            self.db_results1.dsn["dbname"],
            self.db_results2.dsn["dbname"],
        ]
        table.add_rows(self.different_settings)
        print(table)
