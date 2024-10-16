python -m src.main\
    --task abstask\
    --model "gpt-3.5-turbo-instruct"\
    --scheduler parallel\
    --question '{
        "rules": [
            {
                "source": ["N1"],
                "target": ["N2"],
                "time": 3
            },
            {
                "source": ["N6"],
                "target": ["N3"],
                "time": 4
            },
            {
                "source": ["N2", "N3"],
                "target": ["N4"],
                "time": 2
            },
            {
                "source": ["N4"],
                "target": ["N5"],
                "time": 1
            },
            {
                "source": ["N2"],
                "target": ["N5"],
                "time": 5
            }
        ],
        "initial_source": ["N1", "N6"],
        "target": "N5"
    }'