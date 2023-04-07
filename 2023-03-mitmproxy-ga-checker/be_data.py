from tools.functions import parse_ga_key

# BE Hostname
be_hostname = 'https://www.brilliantearth.com'

# BE Paths List. Will be combined with be_hostname to build a URL list
be_path_list = [
  '/Petite-Elodie-Solitaire-Ring-Gold-BE18959-9027466/',
  '/Secret-Halo-Diamond-Ring-Gold-BE1D13065-6495631/',
  '/Luxe-Viviana-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D129-4054081/',
  '/Petite-Twisted-Vine-Diamond-Ring-(1/8-ct.-tw.)-White-Gold-BE1D54-3821855/',
  '/Petite-Shared-Prong-Diamond-Ring-(1/4-ct.-tw.)-White-Gold-BE1PD25R25-1151393/',
  '/Versailles-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D7890-5512247/',
  '/rings/cyorings/purchase_review/',
  '/Dawn-Diamond-Ring-Gold-BE1D9140-9116209/',
  '/Nadia-Diamond-Ring-Gold-BE1D6013-6977758/',
  '/Lumiere-Diamond-Ring-Gold-BE1D928-3337692/',
  '/Aria-Three-Stone-Diamond-Ring-(1/10-ct.-tw.)-Gold-BE1D232-3354646/',
  '/rings/cyorings/purchase_review/',
  '/Four-Prong-Petite-Comfort-Fit-Solitaire-Ring-Gold-BE1199-1325452/',
  '/Demi-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D305-5423943/',
  '/Waverly-Halo-Diamond-Ring-(1/2-ct.-tw.)-White-Gold-BE1D64-3957961/',
  '/Secret-Garden-Diamond-Ring-(1/2-ct.-tw.)-White-Gold-BE1D6351-8721403/',
  '/Aimee-Diamond-Ring-Gold-BE1D602-11135891/',
  '/rings/cyorings/purchase_review/',
  '/Cometa-Three-Stone-Diamond-Ring-Gold-BE1D032-9883561/',
  '/Elodie-Solitaire-Ring-Gold-BE1D2370-3585312/',
  '/Freesia-Solitaire-Ring-Gold-BE1343-12700468/',
  '/Opera-Three-Stone-Diamond-Ring-White-Gold-BE1D5320-8032928/',
  '/9x7mm-Super-Premium-Oval-Moissanite-MO9X7OV1/?process=cyoring',
  '/Luxe-Viviana-Diamond-Ring-(1/3-ct.-tw.)-Gold-BE1D129-4054082/',
  '/Luxe-Sienna-Halo-Diamond-Ring-(3/4-ct.-tw.)-White-Gold-BE1D460-3958243/',
  '/Tapered-Baguette-Three-Stone-Diamond-Ring-Gold-BE503TB230-1151719/',
  '/Viviana-Diamond-Ring-(1/4-ct.-tw.)-White-Gold-BE1D1260-7876326/',
  '/8mm-Super-Premium-Round-Moissanite-MO8.0RD1/?process=cyoring',
  '/customize-mens-wedding-bands/',
  '/Petite-Elodie-Solitaire-Ring-White-Gold-BE18959-9027465/',
  '/rings/cyorings/purchase_review/',
  '/rings/cyorings/purchase_review/',
  '/Versailles-Diamond-Ring-(1/3-ct.-tw.)-Gold-BE1D7890-5512248/',
  '/Aria-Three-Stone-Diamond-Ring-(1/10-ct.-tw.)-White-Gold-BE1D232-3354645/',
  '/rings/cyorings/purchase_review/',
  '/Petite-Comfort-Fit-Six-Prong-Solitaire-Ring-Gold-BE1199H6-1912137/',
  '/Secret-Garden-Diamond-Ring-(1/2-ct.-tw.)-Rose-Gold-BE1D6351-8721405/',
  '/Adorned-Opera-Three-Stone-Diamond-Ring-(1/2-ct.-tw.)-Gold-BE1D322-12694822/',
  '/Petite-Viviana-Diamond-Ring-(1/6-ct.-tw.)-White-Gold-BE1D6912-8671637/',
  '/rings/cyorings/purchase_review/',
  '/Four-Prong-Petite-Comfort-Fit-Solitaire-Ring-White-Gold-BE1199-1325451/',
  '/rings/cyorings/purchase_review/',
  '/Petal-Diamond-Ring-Gold-BE1D1614-10243379/',
  '/Gala-Diamond-Ring-White-Gold-BE1D6362P-9634461/',
  '/Camellia-Diamond-Ring-Gold-BE1D2468-13470584/',
  '/rings/cyorings/purchase_review/',
  '/rings/cyorings/purchase_review/',
  '/2mm-Comfort-Fit-Solitaire-Ring-White-Gold-BE101-1151785/',
  '/Petite-Luxe-Twisted-Vine-Diamond-Ring-(1/4-ct.-tw.)-White-Gold-BE1M55D-1153190/',
  '/Adorned-Dawn-Diamond-Ring-Gold-BE1D1438-14488330/',
  '/Toi-et-Moi-Morganite-and-Pink-Tourmaline-Cocktail-Ring-Gold-BE2MO500/',
  '/Petite-Elodie-Solitaire-Ring-Platinum-BE18959-9027468/',
  '/Sydney-Perfect-Fit-Diamond-Ring-Gold-BE1D17651-16828234/',
  '/Petite-Twisted-Vine-Three-Stone-Diamond-Ring-(2/5-ct.-tw.)-White-Gold-BE1M30D-3015415/',
  '/rings/cyorings/purchase_review/?ucg=true',
  '/Petite-Secret-Halo-Diamond-Ring-White-Gold-BE1D3108-17281912/',
  '/9x7mm-Lab-Created-Emerald-EMLC9X7EC3/?process=cyoring',
  '/Olympia-Diamond-Ring-White-Gold-BE1D2016-7764761/',
  '/Soiree-London-Blue-Topaz-and-Diamond-Cocktail-Ring-Gold-BE2LBT700/',
  '/Luna-Bezel-Ring-Gold-BE1PB1-1151579/',
  '/Luxe-Petite-Shared-Prong-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1PD28R15-3618493/',
  '/Petite-Demi-Diamond-Ring-(1/5-ct.-tw.)-White-Gold-BE1D1320-12835658/',
  '/rings/cyorings/purchase_review/',
  '/8x6mm-Super-Premium-Oval-Moissanite-MO8X6OV1/?process=cyoring',
  '/Secret-Halo-Diamond-Ring-White-Gold-BE1D13065-6495627/',
  '/Aimee-Solitaire-Ring-Gold-BE14112-12628011/',
  '/Luxe-Secret-Garden-Diamond-Ring-(3/4-ct.-tw.)-White-Gold-BE1D6352-12137267/',
  '/9x7mm-Super-Premium-Emerald-Moissanite-MO9X7EC1/?process=cyoring',
  '/Esme-Solitaire-Ring-Gold-BE1D1961-4886109/',
  '/rings/cyorings/purchase_review/',
  '/Luxe-Viviana-Diamond-Ring-(1/3-ct.-tw.)-Platinum-BE1D129-4054084/',
  '/Opera-Three-Stone-Diamond-Ring-Gold-BE1D5320-8032929/',
  '/Adorned-Petite-Elodie-Diamond-Ring-Gold-BE1D2840-8622904/',
  '/Secret-Garden-Diamond-Ring-(1/2-ct.-tw.)-Gold-BE1D6351-8721404/',
  '/Elle-Solitaire-Ring-Gold-BE1D332-7530804/',
  '/rings/cyorings/purchase_review/',
  '/rings/cyorings/purchase_review/',
  '/Demi-Diamond-Ring-(1/3-ct.-tw.)-Gold-BE1D305-5423944/',
  '/rings/cyorings/purchase_review/',
  '/Waverly-Three-Stone-Diamond-Ring-(3/4-ct.-tw.)-White-Gold-BE1D1859-13631424/',
  '/rings/cyorings/purchase_review/',
  '/Luxe-Opera-Three-Stone-Diamond-Ring-White-Gold-BE1D9008-18127047/',
  '/Simply-Tacori-Three-Stone-Marquise-Diamond-Ring-Gold-BE1DT2685-12921126/',
  '/rings/cyorings/purchase_review/',
  '/rings/cyorings/purchase_review/',
  '/Toi-et-Moi-London-Blue-Topaz-and-Lab-Alexandrite-Cocktail-Ring-Gold-BE2LBT800/',
  '/rings/cyorings/purchase_review/',
  '/Round-Diamond-Stud-Earrings-(1-ct.-tw.)-White-Gold-BE304RD100/',
  '/Petite-Twisted-Vine-Diamond-Ring-(1/8-ct.-tw.)-Gold-BE1D54-3821856/',
  '/Petite-Shared-Prong-Diamond-Ring-(1/4-ct.-tw.)-Gold-BE1PD25R25-1151392/',
  '/Sora-Diamond-Ring-Gold-BE1D4488-10020346/',
  '/9x7mm-Super-Premium-Radiant-Moissanite-MO9X7RA1/?process=cyoring',
  '/Luxe-Versailles-Diamond-Ring-(1/2-ct.-tw.)-White-Gold-BE1D626-12722104/',
  '/rings/cyorings/purchase_review/',
  '/rings/cyorings/purchase_review/',
  '/Festivity-Prasiolite-and-Diamond-Cocktail-Ring-Gold-BE2GAM100/',
  '/Joy-Halo-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D4631-3755106/',
  '/Petite-Opera-Three-Stone-Diamond-Ring-(1/4-ct.-tw.)-White-Gold-BE1D804-12003305/',
  '/Nadia-Diamond-Ring-White-Gold-BE1D6013-6977754/',
  ]

# Test path for tools.parse_ga_key
test_ga_path = "/g/collect?v=2&tid=G-M6K9G20MZ3&gtm=45je3360&_p=596304007&cid=345498148.1677184405&ul=en-us&sr=1920x1080&uaa=arm&uab=64&uafvl=Chromium%3B110.0.5481.177%7CNot%2520A(Brand%3B24.0.0.0%7CGoogle%2520Chrome%3B110.0.5481.177&uamb=0&uam=&uap=macOS&uapv=13.2.1&uaw=0&_eu=IA&_s=1&cu=USD&sid=1678305777&sct=17&seg=1&dl=https%3A%2F%2Fwww.brilliantearth.com%2FNadia-Diamond-Ring-Gold-BE1D6013-6977758%2F&dt=Cluster%20Accent%20Diamond%20Ring%20%7C%20Nadia%20%7C%20Brilliant%20Earth&en=view_item&pr1=k0style~v0Modern%20Collection%2CNature%20Collection~id6977758~nm18K%20Yellow%20Gold%20Nadia%20Diamond%20Ring~pr1150.00~va18K%20Yellow%20Gold~brBrilliant%20Earth~k1item_sku~v1BE1D6013-18KY~lp1~caEngagement%20Rings~c2CYO~c3Three%20Stone~c4Three%20Stone~c5&ep.value=1150.00"

# Test URL for tools.go_to_url
test_url = 'https://www.brilliantearth.com/Secret-Halo-Diamond-Ring-Gold-BE1D13065-6495631/'


# Smaller RL Test Lists for debugging
# parse_ga_key() is used here to test if it can parse and decode the URL from the query string parameter of the GA URL. 'dl' is the key for the URL the GA Tag is for.
url_test_list1 = [
  'https://www.brilliantearth.com/Secret-Halo-Diamond-Ring-Gold-BE1D13065-6495631/', # 🟢
  parse_ga_key(test_ga_path, 'dl'), # 🟢
  'https://example.com/',
  'https://www.brilliantearth.com/Versailles-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D7890-5512247/', # 🟢
  'https://www.brilliantearth.com/Petite-Twisted-Vine-Diamond-Ring-(1/8-ct.-tw.)-White-Gold-BE1D54-3821855/' # 🟢
]

url_test_list2 = [
  'https://www.brilliantearth.com/Secret-Halo-Diamond-Ring-Gold-BE1D13065-6495631/',
  parse_ga_key(test_ga_path, 'dl'),
  'https://www.brilliantearth.com/Versailles-Diamond-Ring-(1/3-ct.-tw.)-White-Gold-BE1D7890-5512247/'
]

url_test_list3 = [
    be_path_list[0],
    be_path_list[1],
    be_path_list[2],
    be_path_list[3],
    be_path_list[4],
]