# Hardware
Some parts have been bought already, others I would like to finish the software for it before buying


## Board
The system runs on a Raspberry Pi 4b (refered to as RPI)

## Power Supply
From the wall, a [12v AC-DC converter][1] ($10) makes up to 5A\
The wires go into [Wago Connectors][2] ($8) to split into a set for the Amplifier and the RPI, this happens both for the positive and negative ends\
The amplifier takes 12v, so that wire can be direct. The wires to the RPI go into a [12v to 5v DC-DC USB-C][3] ($12), which can handle 5A. The RPI setup should not need more than 25w

## Display
A [3.2 Inch IPS LCD display at 800x480px][4] ($28.51) Sits right on the Pi with a nice Mini-HDMI to HDMI connector. Either USB-C power connection or Pogo pins to the RPI 5v (I will be using pogo) 

## Audio
I tore apart some $7 speakers from Goodwill to get 2 10watt 4ohm speakers.\
To go with them I will be using this [15w+15w PAM8620 Amplifier][5] With 12v input for power and 3.5mm for sound. It is made for 8ohm speakers, but claims to limit to 15w for 4ohm connections. I will adjust the potentiometer to as high as sounds good with the RPI sound maxed, so that I can secure the potentiometer there and adjust volume digitally from the RPI

## Light
A cool feature I saw on some other high end alarm clocks was a light that slowly turns on to mimic the sun coming up. I would like to integrate this with either a color filtered LED or an RGB led so that the light is a warmer hue

## Buttons
I mess around with keyboards, and I had some spare mechanical switches laying around. It should be as simple as connecting wires to GPIO pins through the switch to GND. Wires are ordered and on the way
### Configuration/Layout
Button 1 (17): Click for pause/play or dismiss (if an alarm is active)
Button 2 (27): Click to tell Media API to toggle Bluetooth connection
Button 3 (22): Click for next song or snooze (if alarm is active)


[1]: https://www.amazon.com/110-240V-Converter-Transformer-Compatible-5-5x2-1mm/dp/B0CPLQH2YP/ref=sr_1_5?crid=T0ZL9ZNGC65Q&dib=eyJ2IjoiMSJ9.rmoRR3N5w4LuqVPr1dgj5iD5eJfOvSjYX35IUVf99MH75j6IezYNj-AOGy_c2gaE2Aq_0jzmwcHKfT2FtYpg9OPDxkzMqHLT6XUDz_oHj4ZKfGeRs_pliWfX-bQPWgjxUYrFHDcAHC0_T_EHw4hQ-lBzIq5FaPIY9oIDOL57Vl_3ufPf5yDZlQqaCwd6S3sg65J7001lGvwvdcn0TDHTVWD9KAcJCQfRncQx8NHM2AUNvnTLXgW_20zCshmFON3oeUN8ezBxstw-Zhe4dirX7g-rcz32jaM8Z51pdzrLAAQ.Iten39j6UIQCnik-QxyJu6cvDRAvOoUJwWNSWR5MObI&dib_tag=se&keywords=12v+power+supply&qid=1715994382&refinements=p_n_feature_eight_browse-bin%3A41942721011&rnid=41941869011&s=electronics&sprefix=12v+%2Caps%2C121&sr=1-5
[2]: https://www.amazon.com/WAGO-221-413-Lever-Nuts-3-Conductor-Connectors/dp/B07W94XJSN/ref=sr_1_2?crid=1CPCRKKQP200Y&dib=eyJ2IjoiMSJ9._n-3B64EWEIacoNY230pLKuL40t1fcx7OiEvmluGasjBs-JwkdIQZGK2gzhR0_fQIrZn6XdN4DeZk7z0RmQqTHRGuvyVLwEre3RbrSy_V5FBpOH1sVko1MWlcvkpQvwmwXd3N6xwCAC9CKBkIc9KFsO3u-_BELMdFcApDZSTsYAwjRP7ulfnf8cBV7S0aK4ovhWXmAjpddtCjXO8viMEB8amnZbDwDk2yIM4hibLCWs.I_LIT7HRI0IgRebbjO-0IDY29HRb5hwXce7DquIHzgk&dib_tag=se&keywords=Wago+221-413+Lever-Nuts+3&qid=1715996042&sprefix=wago+221-413+lever-nuts+3%2Caps%2C146&sr=8-2
[3]: https://www.amazon.com/Klnuoxj-Converter-Interface-Waterproof-Compatible/dp/B0CRVW7N2J/ref=sr_1_6?crid=1UI8HJXC7QFEP&dib=eyJ2IjoiMSJ9.ZkbI94MflLSOS3hox8gmtdN75M9aOcIfSTIE1SPlthXgZbHXnCRDAxy1erPivv45Cs2Gyyrivtalw2q20VBzUpUBmh66FCDnPehXuy32VeWPye5pFEDlxWwCybwQnS2P_KVTiU__pXKcScYX7P7XSTA175JZupbo5c0roDz2ajMOLTUiKKxiMVszvFjrjP1yTHwXLn1fqeZ8Gcu53VWIhbEy7vFIfbCteOfOaBQHjus.uhmdYUG1UxHYDUkb3dKDKoo-l9CEZhXt8Lsl1Cv7A5E&dib_tag=se&keywords=12v%2Bto%2B5v%2Busb%2Bc&qid=1715993962&sprefix=12v%2Bto%2B5v%2Busb%2Caps%2C122&sr=8-6&th=1
[4]: https://thepihut.com/products/3-2-ips-hdmi-lcd-display-for-raspberry-pi-480x800
[5]: https://www.amazon.com/Amplifier-DROK-PAM8406-Digital-Channel/dp/B077M526SB/ref=pd_scr_dp_alt1_d_d_sccl_2_1/131-4225016-5819016?pd_rd_w=bHRgO&content-id=amzn1.sym.443fa366-3c43-4184-b722-e4a18524387a&pf_rd_p=443fa366-3c43-4184-b722-e4a18524387a&pf_rd_r=HRSDF4G5SHNZWHANR1NJ&pd_rd_wg=s8yV9&pd_rd_r=fd43f38d-12c8-4ff1-8fe3-b99704c05154&pd_rd_i=B077MKQJW2&th=1
