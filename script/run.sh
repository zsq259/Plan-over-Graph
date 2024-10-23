python -m src.main\
    --task abstask\
    --model "gpt-3.5-turbo-instruct"\
    --scheduler parallel\
    --question '''{
        "id": 2,
        "question": {
            "rules": [
                {
                    "source": [
                        "N1"
                    ],
                    "target": [
                        "N2"
                    ],
                    "time": 3,
                    "cost": 1
                },
                {
                    "source": [
                        "N1",
                        "N2"
                    ],
                    "target": [
                        "N3"
                    ],
                    "time": 2,
                    "cost": 1
                },
                {
                    "source": [
                        "N2"
                    ],
                    "target": [
                        "N4"
                    ],
                    "time": 5,
                    "cost": 1
                },
                {
                    "source": [
                        "N1"
                    ],
                    "target": [
                        "N5"
                    ],
                    "time": 2,
                    "cost": 1
                },
                {
                    "source": [
                        "N2"
                    ],
                    "target": [
                        "N5"
                    ],
                    "time": 1,
                    "cost": 1
                },
                {
                    "source": [
                        "N5"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 1,
                    "cost": 1
                },
                {
                    "source": [
                        "N3"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 2,
                    "cost": 1
                },
                {
                    "source": [
                        "N4"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 1,
                    "cost": 1
                },
                {
                    "source": [
                        "N2"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 3,
                    "cost": 1
                },
                {
                    "source": [
                        "N1"
                    ],
                    "target": [
                        "N6"
                    ],
                    "time": 4,
                    "cost": 1
                },
                {
                    "source": [
                        "N2",
                        "N1",
                        "N5"
                    ],
                    "target": [
                        "N7"
                    ],
                    "time": 5,
                    "cost": 1
                },
                {
                    "source": [
                        "N4"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 5,
                    "cost": 1
                },
                {
                    "source": [
                        "N5"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 1,
                    "cost": 1
                },
                {
                    "source": [
                        "N7"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 3,
                    "cost": 1
                },
                {
                    "source": [
                        "N3"
                    ],
                    "target": [
                        "N8"
                    ],
                    "time": 5,
                    "cost": 1
                }
            ],
            "initial_source": [
                "N1"
            ],
            "target": "N6"
        },
        "answer": 3
    }'''