"""Regression: inner ambassador content must fit the visible outer card."""
from browser_check import Driver

driver = Driver()
try:
    for width in (1440, 1024, 390):
        driver.resize(width, 1100)
        driver.navigate('http://100.125.15.37:8080/index.html')
        from time import sleep
        sleep(0.6)
        result = driver.execute('''
          const card = document.querySelector('.initiative-slide.is-active');
          const panel = card.querySelector('.initiative-ambassadors');
          const a = card.getBoundingClientRect(), b = panel.getBoundingClientRect();
          return {cardBottom:a.bottom, panelBottom:b.bottom, fits:b.bottom <= a.bottom - 8};
        ''')
        print(width, result)
        assert result['fits'], result
        driver.execute("document.querySelector('.initiatives-carousel').scrollIntoView({block:'center',behavior:'instant'})")
        from pathlib import Path
        driver.screenshot(Path(f'/home/kai/General/work/IYOF/ambassador-fixed-{width}.png'))
finally:
    driver.close()
