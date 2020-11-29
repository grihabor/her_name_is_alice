import os
from contextlib import contextmanager, ExitStack
from tempfile import TemporaryDirectory
from typing import ContextManager

import matplotlib.pyplot as plt
import pandas as pd
import click


COLUMN_NUMBER_OF_PERSONS = "NumberOfPersons"
COLUMN_NAME = "Name"
COLUMN_YEAR = "Year"


def count_grouped(data, *, name: str):
    name_rows = count_grouped_by_year_name(data).reset_index()
    name_rows = name_rows[name_rows[COLUMN_NAME] == name]
    name_rows = name_rows.set_index(COLUMN_YEAR)[[COLUMN_NUMBER_OF_PERSONS]]
    all_rows = count_grouped_by_year(data)
    ratio = name_rows / all_rows

    return pd.concat(
        [
            name_rows.rename(columns={COLUMN_NUMBER_OF_PERSONS: "name"}),
            all_rows.rename(columns={COLUMN_NUMBER_OF_PERSONS: "all"}),
            ratio.rename(columns={COLUMN_NUMBER_OF_PERSONS: "ratio"}),
        ],
        axis=1,
    )


@click.command()
@click.option("-s", "--separator", default=";")
@click.option("-e", "--encoding", default="windows-1251")
@click.option("-n", "--name", default="Надежда")
@click.argument("path", type=click.Path(exists=True))
def main(path, separator, encoding, name):

    with fix_csv(path, encoding=encoding) as fixed:
        data = pd.read_csv(fixed, sep=separator, dtype={COLUMN_NUMBER_OF_PERSONS: int})

    ratio = count_grouped(data, name=name)

    click.echo(ratio, err=True)

    plt.plot(ratio.index, ratio["ratio"])
    output_path = "ratio.svg"
    plt.savefig(output_path)

    click.echo(output_path)


def count_grouped_by_year_name(df):
    df = df[[COLUMN_NUMBER_OF_PERSONS, COLUMN_YEAR, COLUMN_NAME]]
    return df.groupby([COLUMN_YEAR, COLUMN_NAME]).sum()[[COLUMN_NUMBER_OF_PERSONS]]


def count_grouped_by_year(df):
    df = df[[COLUMN_NUMBER_OF_PERSONS, COLUMN_YEAR]]
    return df.groupby([COLUMN_YEAR]).sum()[[COLUMN_NUMBER_OF_PERSONS]]


@contextmanager
def fix_csv(path: str, *, encoding: str) -> ContextManager[str]:
    with TemporaryDirectory() as d:
        tmp_path = os.path.join(d, "data.csv")

        with ExitStack() as es:
            src = es.enter_context(open(path, "r", encoding=encoding))
            dst = es.enter_context(open(tmp_path, "w"))

            src_it = iter(src)
            first_line = next(src_it)
            dst.write(first_line)
            for line in src_it:
                if line == first_line:
                    continue

                dst.write(line)

        yield tmp_path


if __name__ == "__main__":
    main()
