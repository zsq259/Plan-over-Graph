python -m src.main\
    --task abstask\
    --model "meta-llama/Llama-3.2-1B-Instruct"\
    --scheduler parallel\
    --question '''{
    "question": {
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
    }
}'''