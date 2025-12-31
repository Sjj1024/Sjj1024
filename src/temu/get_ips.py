#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""
获取私密代理IP
"""

import requests

# 获取私密代理IP API
api = "https://dps.kdlapi.com/api/getdps"

# 请求参数
params = {
    "secret_id": "or67jn7d4eam4s7zzqnk",
    "signature": "1111",
    "num": 2,  # 提取数量
}

# 获取响应内容
response = requests.get(api, params=params)
print(response.text)

url_list = [
    "https://www.douyin.com/user/MS4wLjABAAAAH_YSjSBpUOItBNIP5B3B235ER7GUYgJ1qnkpKPF2kKc?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAASVa-8R_3SGeSaJudPW8WD-cUJVqxnvFtcPjH66IESVo?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAB4ZzUOvRnFkCATQaFNMTKaGGWrEPWhdyTMdP0hTQNpmgdbfvrWwmowP0phinRkef?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAd23jWkNJ2yPXAQseofIP-mEdScK7NhS5LFQun6nIjhs?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAnsr6J6jnubMTqFpkFDdC7yqGPAM1MNHXlwwrVtxTbc_r616UzLlXePcD2vOirDOy?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAPBx6r-AoPT1XvjR_rGCxO-Qmr193ku_gP45kzfLvyq2vNOyd_r95KgnWdxPJ7geh?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAJ05N_nIVmPyh7oh64ErkFgS8q89hcWh3XmxvNeDX2b3ULsoUzCYD5_KZz9roVSfX?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAe71N0mRXX9GPC4qW5oGq7bDplwdYTiJxwvdTqGSkuQiB7YMCMiJExY0iq6cEnuwR?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAw7gvr89_FSreJfRenI1Qrc93w3vcXYEMvO7-VErZzvbfE8tVQpm8kMJwtU22j0yu?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAATsv_m9qEYXU0IEz4ENmf7spXYkK-ft8gaCixS9gD2a24BA_Wxcoq2XjpvbrKpJQl?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAesgJnnrETWDV8nySSLTBq0hJx1GseK8F8HDpQx-D7a5RMOCdGiiP6xIl56_C8q0b?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAA4DJhT9ORR1TXSbsMlxJzfHWEM0BrHbgNF6347-H_N80FZtO18w3vd3rqhAI6wOm-?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAz26MVwwUQ7Jz3eMcbVOhr1JkiHF-S26WjWgQxKkG_02PK-ym-0_SLlmHeZhVINXT?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAs_zRTA_9DULL-UGrjq-BV9yd16HPCsRYW0FhDXWLzk5HqGSg0zgVt_e-H3Xy8Ka4?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAG0WERc4bKmeTwLgnWBqDz7k0azeqGdmUHIDuyPpi2Bs?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAEc_2ABSTGyu1L9dj5xZrI6Da9FtkCOgtZ3aY-sS_I4uIn73sCaAxyT4jCu-BQz9d?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAPzyVhl-NWnh693FCkbNY6mLDPt2PYzv87TRBjezBX0ow4jrQ4BGGejxTCrmX3IQ2?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAck0b2cg8gQUNhp5ttJ12ucjHI5kqbMdo6Yrp6ZbTTMsnkVunAL0-EQXjNeCnOCB_?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAeS_Xrleiy_XFufKG5BGrA1ZdCojLMNAW9V1dSKyzc1yGSyzmLaQM0xTWM7fWjiqe?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAe-AlpiH4a8dabNN3DEVTn5M0pHj45myU_QgFm04drOypfyJYwbEXAhhUnioCLjey?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAATUbgBHReE9Zw3MiYlMIzQxOnHDwCHCzbmPg2eKp0Aqs?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAA6qX49JCUNyk_xmezYU_SssK5Uq4c7rGz66_S_U9Duodd6LC3ztXoxFVryBpddcc8?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAaUPI2ZtKblsLXc1CQrcGHT-8QoquH0SOrt51j-BIBc4?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAdv-R52269bQliOHzJJkEeJ-ueYe112p4_5L4Vrd7iy1tIgDt3X6nb395xOARspww?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAEsnIf1fXR2Xt9hF-cy17cUQYjBsgAIe5h9p-raEmr6Y?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAzFwSM25Nd20LJ1rhPpvSbhw6dR0vwaVbap74VqzmZqbutJRHDpWtHZxoAddaVOZk?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAA-crcQAJtoOVl3f59ji4zsMb4yUUFwQ7yUHZdN5V3sEv1fZ_gbUDGAqO67sI5sUxL?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAA_sogcZOHtAA8FOw4k4cfe2Ya4pdSadjmTRRQzfyLO1Q?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAJeDvStB201SHYCutq_s61pZcu640lxtPKsC8mLWLbz4hK_rFMvzi7HFjsaS3yu6i?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAATIjOtKTp9434oRlrK8y7zqevYoB_IuUNgDI58ie0ups?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAykLKsc6vST0iWgJP6zxijMFYzoAr8UfLnv_pek4oxLJ38Lq8FmDUjKf20c5c1lIn?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAoXm3UTY6L_aOBfJxd0Y8B9ojQS4rUUWwDK-iEre3opQ?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAOUAXXKImDTIJuTUhQ-1r5V8R8xNSTPuZO_jX8a2Zd60?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAArSnivWCSP4NPPhXHjcqIZdx6hXu46hB7iSsdcaFM0wM?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAykLKsc6vST0iWgJP6zxijMFYzoAr8UfLnv_pek4oxLJ38Lq8FmDUjKf20c5c1lIn?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAFiegzOpngguZ0Lxh_A6OwYPZANrmsRH5s0YCIsFtZn4?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAndmaE0jpzMZHWno8eVnCY7gZnDUOZ6ivx86DOzK3onOALlyBR84pUfODVnMLF6eE?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAgg6CPXOihH4rtxHceUb-80QZayrld3a-4jV1PP6gMh8?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAFKe0CylnXN3oCDDUpQ4BJSpzN7J5VJuxvJErMWJjxQMmZ2T4cN07we6vNGrnUsGc?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAD0AOGkuktCcPT4oJA0XJ-Fv6-cJCvjGXVhFG18lvkL_4sbz1YKNbNIFO33zd2Ohi?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAArd33_DkZRpjJ1SLdyfmakLGaAKrEuru3lbERGZczqlfc60SnSO5lxImkWoG2dQMl?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAA9KWmWHOjwD_NJ7bRTi_J8Uwu1ZifEYRwjMPw3Z_twm4?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAQ5VdtpwWgUk1Xi6qrSWS2DWvvKi0RpVZr_FTedMwxg0?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAI5Nq3bV88dTg3czTHPL4gFPIpBlAalCM1dyyS4CSEQH6XhbIO6U8aJh8dFhxHOra?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAATVXT5wBrGRldaOw9O07GHer-muC3zDIfMYjxXkEQPq3IDrrsBLkPnd4ksRK2-wV3?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAGqiizbJdmeMyqKXHiexsGVCyivGiqH6yztdYvjw3r4uBdxBbHVeGw6zjrtgsBM69?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAADMGKFxRyU4upsAMC2q10fTJHwa-ISsLuZ_sOjmiw3actdY6NAazOifdHhvjNzapX?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAOorS-WPIa7GZnRLBiZczeHNreeGI_cGxTHuSbfzKVXM?from_tab_name=main",
    "https://www.douyin.com/user/MS4wLjABAAAAWI6yRSUNtZQkFIPdKZbeY4UV3Bhisktka1RiWf7XgJk?from_tab_name=main",
]