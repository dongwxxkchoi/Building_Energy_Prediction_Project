
      @REM Shoeboxer GenCumulativeSky
      SET RAYPATH=.;C:\umi\Radiance\lib;C:\umi\Radiance\bin;C:\umi\Daysim\bin_windows;$RAYPATH
      SET PATH=.;C:\umi\Radiance\lib;C:\umi\Radiance\bin;C:\umi\Daysim\bin_windows;$PATH
      c:
      cd C:\umi\temp\energy\umi_test_0/umi_test_0
      @REM Root Name = 'umi_test_0'
      GenCumulativeSky +s2 -a 33 -o 112 -m 105 -p -E -time 0 24 -date 1 1 12 31 "C:\Users\dwcho\AppData\Local\Temp\umi.session.lahyzpx5.wyg\KOR_SO_Seoul.WS.471080_TMYx.2007-2021.epw" > C:\umi\temp\energy\umi_test_0/umi_test_0\GenCumSky.cal

      oconv -f C:\umi\temp\energy\umi_test_0/umi_test_0\GenCumSky.rad "C:\Umi\default-libraries\DefaultRadianceLibrary.rad" C:\umi\temp\energy\umi_test_0/umi_test_0\GenCumSkyScene.rad > C:\umi\temp\energy\umi_test_0/umi_test_0\GenCumSkyScene.oct