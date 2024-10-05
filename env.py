CMD_MSG: str = (
    "Incorrect cmd input!\nUsage: python main.py <arg>\narg options: ladder, players, team_stats"
)

ENV = {
    "players": {"comp_id": 111},
    "team_stats": {
        "comp_id": 111,
        "year": 2024,
        "stat_ids": [
            3,
            4,
            9,
            28,
            29,
            30,
            31,
            32,
            33,
            35,
            37,
            38,
            69,
            76,
            78,
            81,
            82,
            1000000,
            1000002,
            1000003,
            1000004,
            1000015,
            1000025,
            1000026,
            1000028,
            1000034,
            1000037,
            1000038,
            1000079,
            1000112,
            1000209,
            1000210,
            1000415,
        ],
    },
    "ladder": {"comp_id": 111, "year": 2024, "round": 27},
}
