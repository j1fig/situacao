import pytest

import parse


@pytest.mark.parametrize(
    "line,m,c",
    [("Sever do Vouga 43", "Sever do Vouga", 43), ("Silves 38\u200b", "Silves", 38),],
)
def test_parse_line(line, m, c):
    assert parse._parse_line(line) == (m, c)


@pytest.mark.parametrize(
    "text,lines",
    [
        (
            """Setúbal 83\n
        Sever do Vouga 43\n
        CONCELHO\n
        NÚMERO\n
        DE CASOS\n
        Silves 24\n
        Sintra 1006\n
        4\n
        Sobral de Monte\n
        Agraço\n
        Soure 24\n
        Tábua 35\n""",
            [
                "Setúbal 83",
                "Sever do Vouga 43",
                "Silves 24",
                "Sintra 1006",
                "4",
                "Sobral de Monte",
                "Agraço",
                "Soure 24",
                "Tábua 35",
            ],
        ),
        (
            """Vimioso 10\n
        Vinhais 30\n
        Viseu 99\n
        Vizela 131\n
        Vouzela 8\n
\n
        Reguengos de\n""",
            ["Vimioso 10", "Vinhais 30", "Viseu 99", "Vizela 131", "Vouzela 8",],
        ),
    ],
)
def test_filter_uninteresting_lines(text, lines):
    assert parse._filter_uninteresting_lines(text) == lines


@pytest.mark.parametrize(
    "lines,coalesced",
    [
        (
            [
                "Setúbal 83",
                "Sever do Vouga 43",
                "Silves 24\u200b",
                "Sintra 1006",
                "4",
                "Sobral de Monte",
                "Agraço",
                "Soure 24",
                "Tábua 35",
            ],
            [
                "Setúbal 83",
                "Sever do Vouga 43",
                "Silves 24",
                "Sintra 1006",
                "Sobral de Monte Agraço 4",
                "Soure 24",
                "Tábua 35",
            ],
        ),
        (
            [
                "Vila Nova de Poiares 6",
                "Vila Pouca de Aguiar 6",
                "Vila Real 151",
                "Vila Real de Santo",
                "António",
                "13",
                "Vila Verde 228",
                "Vimioso 10",
                "Vinhais 30",
            ],
            [
                "Vila Nova de Poiares 6",
                "Vila Pouca de Aguiar 6",
                "Vila Real 151",
                "Vila Real de Santo António 13",
                "Vila Verde 228",
                "Vimioso 10",
                "Vinhais 30",
            ],
        ),
    ],
)
def test_coalesce_lines(lines, coalesced):
    assert parse._coalesce_lines(lines) == coalesced


@pytest.mark.parametrize(
    "lines,counts,leftovers",
    [
        (
            [
                "Setúbal 83",
                "Sever do Vouga 43",
                "Silves 24",
                "Sintra 1006",
                "4",
                "Sobral de Monte",
                "Agraço",
                "Soure 24",
                "Tábua 35",
            ],
            [83, 43, 24, 1006, 4, 24, 35,],
            [
                "Setúbal",
                "Sever do Vouga",
                "Silves",
                "Sintra",
                "Sobral de Monte",
                "Agraço",
                "Soure",
                "Tábua",
            ],
        ),
        (
            [
                "Vila Nova de Poiares 6",
                "Vila Pouca de Aguiar 6",
                "Vila Real 151",
                "Vila Real de Santo",
                "António",
                "13",
                "Vila Verde 228",
                "Vimioso 10",
                "Vinhais 30",
            ],
            [6, 6, 151, 13, 228, 10, 30,],
            [
                "Vila Nova de Poiares",
                "Vila Pouca de Aguiar",
                "Vila Real",
                "Vila Real de Santo",
                "António",
                "Vila Verde",
                "Vimioso",
                "Vinhais",
            ],
        ),
    ],
)
def test_extract_counts(lines, counts, leftovers):
    assert parse._extract_counts(lines) == (counts, leftovers)
