def slacs_keys_list_from():

    return [
        "slacs2341+0000",
        "slacs0946+1006",
        "slacs0956+5100",
        "slacs1020+1122",
        "slacs1032+5322",  # Index 21
        "slacs0959+0410",
        "slacs1432+6317",
        "slacs1250+0523",
        "slacs1143-0144",
        "slacs0029-0055",
        "slacs0330-0020",
        "slacs0912+0029",  # Index 11
        "slacs1430+4105",
        "slacs1023+4230",
        "slacs0822+2652",
        "slacs0252+0039",
        "slacs1205+4910",
        "slacs0903+4116",
        "slacs1630+4520",
        "slacs1213+6708",
        "slacs2303+1422",
        "slacs0728+3835",  # Index 6
        "slacs1420+6019",
        "slacs1029+0420",
        "slacs1451-0239",
        "slacs2238-0754",
        "slacs0157-0056",
        "slacs1525+3327",
        "slacs1218+0830",
        "slacs1142+1001",
        "slacs0216-0813",
        "slacs1627-0053",
        "slacs2300+0022",
        "slacs0737+3216",
        "slacs1402+6321",
        "slacs0008-0004",
        "slacs0936+0913",
    ]

def consistent_list_from():

    return [
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\checkmark",
        r"\ding{55}",
        r"\ding{55}",
        r"",
        r"",
        r"",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]


def slacs_keys_success_list_from():

    return [
        "slacs2341+0000",
        "slacs0946+1006",
        "slacs0956+5100",
        "slacs1020+1122",
        "slacs1032+5322",  # Index 21
        "slacs1432+6317",
        "slacs1250+0523",
        "slacs0959+0410",
        "slacs1143-0144",
        "slacs0912+0029",  # Index 11
        "slacs0029-0055",
        "slacs0330-0020",
        "slacs1023+4230",
        "slacs1430+4105",
        "slacs0822+2652",
        "slacs0252+0039",
        "slacs1205+4910",
        "slacs0903+4116",
        "slacs1213+6708",
        "slacs2303+1422",
        "slacs0728+3835",  # Index 6
        "slacs1420+6019",
    ]


def slacs_snr_dict_from():

    return {'slacs0008-0004': 8.344803512965093, 'slacs0029-0055': 23.17925439035878, 'slacs0157-0056': 5.582496930656176, 'slacs0216-0813': 15.407697113567847, 'slacs0252+0039': 18.417897365766482, 'slacs0330-0020': 48.72926792734068, 'slacs0728+3835': 12.537742796196715, 'slacs0737+3216': 28.72751219838226, 'slacs0822+2652': 10.541316711809353, 'slacs0903+4116': 10.559348306964688, 'slacs0912+0029': 8.670816239670819, 'slacs0936+0913': 8.104651562457828, 'slacs0946+1006': 27.87418207990507, 'slacs0956+5100': 33.821514735051814, 'slacs0959+0410': 67.5824605245386, 'slacs1020+1122': 11.575066580146704, 'slacs1023+4230': 20.685813429683606, 'slacs1029+0420': 20.18325466500447, 'slacs1032+5322': 49.58917659392757, 'slacs1142+1001': 23.6524787038163, 'slacs1143-0144': 36.25043532592414, 'slacs1205+4910': 38.64282538783859, 'slacs1213+6708': 12.38149468726608, 'slacs1218+0830': 17.54767297828736, 'slacs1250+0523': 15.37617737042003, 'slacs1402+6321': 7.980649681790954, 'slacs1420+6019': 47.134794209251204, 'slacs1430+4105': 39.7407439694325, 'slacs1432+6317': 41.986690685753295, 'slacs1451-0239': 23.893030242372912, 'slacs1525+3327': 10.01, 'slacs1627-0053': 15.008565768251316, 'slacs1630+4520': 20.904886790286405, 'slacs2238-0754': 28.60464227365778, 'slacs2300+0022': 7.639645568757377, 'slacs2303+1422': 19.991786873837643, 'slacs2341+0000': 25.902437134929738}


def slacs_light_fp_from():

    return [
        False, # 1
        False, # 2
        False, # 3
        False, # 4
        False, # 5
        False, # 6
        True,  # New
        False, # 7
        False, # 8
        True, # 9
        False, # 10
        True, # 11
        False, # 12
        True, # 13
        True,  # New
        True, # 14
        True, # 15
        False, # 16
        True,  # New
        True, # 17
        True, # 18
        True, # 19
    ]


def slacs_light_drop_from():

    return [
        True, # 1
        False, # 2
        True, # 3
        True, # 4
        True, # 5
        True, # 6
        True, # 7
        False, # 8
        True, # 9
        False, # 10
        True, # 11
        False, # 12
        False, # 13
        True, # 14
        False, # 15
        False, # 16
        False, # 17
        True, # 18
        True, # 19
    ]


def slacs_source_fp_from():

    return [
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        False,  # 17
        False,
        False,
        True,
        False,
        False,
        False,
        False,
        True,
        False,
        False,
        False,  # 17
        False,
        False,
        False,
        False,
    ]


def slacs_source_drop_from():

    return [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
        False,
        False,
        False,
    ]


def slacs_bpl_drop_from():

    return [
        False, # 1
        False, # 2
        True, # 3
        False, # 4
        False, # 5
        False, # 6
        False, # 7
        False, # 8
        False, # 9
        False, # 10
        False, # 11
        True, # 12
        False, # 13
        False, # 14
        False, # 15
        False, # 16
        False, # 17
        False, # 18
        False, # 19

        True,  # 17
        True,  # 18
        True,  # 19
    ]


def lens_light_pass_list_from():

    return [
        r"\ding{55}",
        r"\checkmark",
        r"\checkmark",
        r"\ding{55}",
        r"\checkmark",
        r"\ding{55}",
        r"\checkmark",
        r"\checkmark",
        r"\ding{55}",
        r"\checkmark",
        r"\ding{55}*",
        r"\ding{55}*",
        r"\checkmark",
        r"\ding{55}*",
        r"\ding{55}*",
        r"\ding{55}*",
        r"\checkmark",
        r"\checkmark",
        r"\ding{55}*",
        r"\checkmark",
        r"",
        r"",
        r"",
        r"",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

def slacs_mass_keys_list_from():

    return [
        "slacs0946+1006",
        "slacs1250+0523",
        "slacs0959+0410",
    ]