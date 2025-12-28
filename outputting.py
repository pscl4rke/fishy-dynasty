

from dataclasses import dataclass


@dataclass
class Output:
    properties: dict


OUTPUTS = {
    # remember any strings will need two levels of quote characters:
    98: Output(  # just on the left-half
        properties={
            "--bg-colour": "#222222",
            "--left-margin": "5%",
            "--right-margin": "50%",
            "--text-colour": "#dddddd",
            "--text-size": "40px",
        },
    ),
    99: Output(  # normal front-of-house
        properties={
            "--bg-colour": "#222222",
            "--left-margin": "0%",
            "--right-margin": "0%",
            "--text-colour": "#dddddd",
            "--text-size": "45px",
        },
    ),
}
