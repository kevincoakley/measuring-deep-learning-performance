import argparse, sys
from jinja2 import Environment, FileSystemLoader

random_seeds = [
    3664629611,
    29616477,
    2934400309,
    3663679676,
    2653170624,
    1717144972,
    3802925187,
    2928815995,
    2852914846,
    3989692623,
    1558099097,
    2229219544,
    1496073244,
    4100528942,
    3105422517,
    2116593738,
    3203774568,
    26449180,
    2247932906,
    1345797628,
    1297055094,
    3388865413,
    3441103961,
    220129177,
    636800229,
    3340778380,
    328826589,
    2351080987,
    2940668278,
    1629467658,
    1374552628,
    2989496591,
    1304254337,
    1160869783,
    1031290362,
    2016501090,
    1419135793,
    328135459,
    725062165,
    698501779,
    2916655170,
    3309567839,
    4282113189,
    293153299,
    2583227991,
    2066139778,
    3453933603,
    3404249524,
    3687309285,
    713197558,
    2549351489,
    2409554458,
    1459005201,
    1051226056,
    4119878508,
    4291492387,
    3140594418,
    777109714,
    1589216892,
    296922354,
    1127772217,
    2586440573,
    2372266162,
    200427186,
    3665818909,
    1051311406,
    4194161626,
    2901435033,
    1027683409,
    2592753973,
    294477085,
    55673650,
    3226759639,
    3130688870,
    3126186108,
    3598909707,
    425796106,
    3442116543,
    2375403279,
    2324886708,
    3564953262,
    1214632149,
    162323494,
    1422274897,
    4214847305,
    4289667837,
    3877990105,
    775343348,
    1572370784,
    2993632363,
    2147810558,
    3359328088,
    1664423657,
    516478726,
    4283274141,
    3472115790,
    1973874623,
    3236139543,
    245344786,
    323245623,
]


def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--runs",
        dest="runs",
        help="Number of run files to create",
        type=int,
        default=10,
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])

    runs = args.runs

    if len(random_seeds) % runs != 0:
        raise ValueError(
            "The number of random seeds must be divisible by the number of runs."
        )

    random_seeds_per_run = int(len(random_seeds) / runs)

    environment = Environment(loader=FileSystemLoader("./"))
    template = environment.get_template("seed-wrapper.sh.j2")

    for run in range(runs):
        filename = f"seed-wrapper-{run}.sh"
        content = template.render(
            random_seeds=random_seeds[
                run * random_seeds_per_run : (run + 1) * random_seeds_per_run
            ],
            run_number=run,
        )
        with open(filename, mode="w", encoding="utf-8") as job:
            job.write(content)
            print(f"Writing: {filename}")
