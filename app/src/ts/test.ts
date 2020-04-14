import { Builder, By, Capabilities, Key, until, WebDriver } from 'selenium-webdriver'

const remote_host = 'selenium-chrome';
const remote_server = `http://${remote_host}:4444/wd/hub`;

const capabilities: Capabilities = Capabilities.chrome()

async function search(query: string): Promise<void> {
  const driver: WebDriver = await new Builder()
    .usingServer(remote_server)
    .withCapabilities(capabilities)
    .build()
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