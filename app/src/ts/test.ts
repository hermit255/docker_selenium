import { By, Key, until, WebDriver } from 'selenium-webdriver'
import { getDriver } from "./modules/getDriver"

async function search(query: string): Promise<void> {
  const driver = await getDriver()
  try {
    await driver.get('https://qiita.com/')
    await driver
      .wait(until.elementLocated(By.name('q')), 5000)
      .sendKeys(query, Key.RETURN)
    const result: string = await driver
      .wait(until.elementLocated(By.className('badge')), 5000)
      .getText()
    console.log(`${query}: ${result}`)
  } catch(e) {
    console.log(e)
  } finally {
    await driver && driver.quit()
  }
}
search('selenium')