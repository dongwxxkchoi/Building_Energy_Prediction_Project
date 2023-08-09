
      @REM Shoeboxer GenCumulativeSky
      SET RAYPATH=.;C:\umi\Radiance\lib;C:\umi\Radiance\bin;C:\umi\Daysim\bin_windows;$RAYPATH
      SET PATH=.;C:\umi\Radiance\lib;C:\umi\Radiance\bin;C:\umi\Daysim\bin_windows;$PATH
      c:
      cd C:\umi\temp\energy\umi_test_0\umi_test_0
      @REM Root Name = 'umi_test_0'
      rtrace -I -h -dp 2048 -ms 0.063 -ds .2 -dt .05 -dc .75 -dr 3 -st .01 -lr 12 -lw .0005 -ab 1 -ad 1000 -as 500 -ar 500 -aa 0.2   C:\umi\temp\energy\umi_test_0\umi_test_0\GenCumSkyScene.oct < C:\umi\temp\energy\umi_test_0\umi_test_0\umi_test_0.pts > C:\umi\temp\energy\umi_test_0\umi_test_0\umi_test_0.dat