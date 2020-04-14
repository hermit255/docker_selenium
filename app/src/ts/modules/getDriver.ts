import { Builder, Capabilities, WebDriver } from 'selenium-webdriver';

const capabilities: Capabilities = Capabilities.chrome();
const remote_host = 'selenium-chrome';
const remote_server = `http://${remote_host}:4444/wd/hub`;

const waitTime: int = 5

export async function getDriver(): WebDriver {
  const driver: WebDriver = await new Builder()
    //.usingServer(remote_server)
    .withCapabilities(capabilities)
    .build();
  driver.implicity_wait
  return driver;
}