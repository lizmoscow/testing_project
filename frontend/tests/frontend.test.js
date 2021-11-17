require('geckodriver');
const { Builder, By, Key, until } = require('selenium-webdriver');

describe("Check main functionality", () => {

  let driver;

  beforeAll(() => {
    const webdriver = require('selenium-webdriver'),
    By = webdriver.By,
    until = webdriver.until;

    driver = new webdriver.Builder()
    .forBrowser('firefox')
    .build();
  })


  it("Loads successfully", () => {
    driver.get('http://127.0.0.1:8000/');

    const element = driver.findElement(By.id('page-title'));
    element.getText().then(function(text) {
      expect(text).toBe('House Party');
    })

    const joinButton = driver.findElement(By.id('join-group'));
    joinButton.click()
        .then(() => {
        driver.sleep(1000) ;
        })
        .then(() => {
        const element = driver.findElement(By.id('page-title'));
        element.getText().then((text) => {
          expect(text).toBe('Join Room');
        })
        const backButton = driver.findElement(By.id('back'));
        backButton.click()
            .then(() => {
              driver.sleep(1000) ;
            })
            .then(() => {
              const createButton = driver.findElement(By.id('create-group'));
              createButton.click()
                  .then(() => {
                    driver.sleep(1000)
                  })
                  .then(() => {
                    const element = driver.findElement(By.id('page-title'));
                    element.getText()
                        .then((text) => {
                          expect(text).toBe('Create Room');
                        })
                    const backButton = driver.findElement(By.id('back'));
                    backButton.click()
                        .then(() => {
                          driver.sleep(1000) ;
                        })
                        .then(() => {
                          const createButton = driver.findElement(By.id('login-button'));
                          createButton.click()
                              .then(() => {
                                driver.sleep(1000)
                              })
                              .then(() => {
                                const element = driver.findElement(By.id('page-title'));
                                element.getText()
                                    .then((text) => {
                                      expect(text).toBe('Sign In');
                                    })
                                const backButton = driver.findElement(By.id('back'));
                                backButton.click()
                                    .then(() => {
                                      driver.sleep(1000) ;
                                    })
                                    .then(() => {
                                      const element = driver.findElement(By.id('page-title'));
                                      element.getText()
                                          .then((text) => {
                                            expect(text).toBe('House Party');
                                          })
                                    })
                              })
                        })
                  })
        })
      })
  })


  it("Can log in successfully", () => {
    driver.get('http://127.0.0.1:8000/login');
    const element = driver.findElement(By.id('page-title'));
        element.getText().then(function(text) {
      expect(text).toBe('Sign In');
    })

    const username = Math.random().toString(36).substr(2, 7)
    const password = Math.random().toString(36).substr(2, 8)
    driver.findElement(By.name('username')).sendKeys(username);
    driver.findElement(By.name('password')).sendKeys(password);
    driver.findElement(By.name('switch')).click();
    driver.findElement(By.name('signin')).click();
    //expect(driver.findElement(By.xpath("//*[text()='Signed up in successfully']")).isDisplayed()).toBeTruthy();
    driver.findElement(By.id('back')).click()
        .then(() => {
            driver.sleep(1000) ;
        })
        .then(() => {
            const element1 = driver.findElement(By.id('page-title'));
            element1.getText().then((text) => {
                expect(text).toBe('House Party with ' + username);
            })
            const logOutButton = driver.findElement(By.id('login-button'));
            logOutButton.click();
            const element2 = driver.findElement(By.id('page-title'));
            element2.getText().then((text) => {
                expect(text).toBe('House Party');
            })
            const logInButton = driver.findElement(By.id('login-button'));
            logInButton.click()
                .then(() => {
                    driver.sleep(1000)
                })
                .then(() => {
                    driver.findElement(By.name('username')).sendKeys(username);
                    driver.findElement(By.name('password')).sendKeys(password);
                    driver.findElement(By.name('signin')).click()
                        .then(() => {
                            driver.sleep(1000)
                        })
                        .then(() => {
                            const element = driver.findElement(By.id('page-title'));
                            element.getText().then((text) => {
                                expect(text).toBe('House Party with ' + username);
                            })
                        })
                })
        })


  })


  it("Can join a room successfully", () =>{
      driver.get('http://127.0.0.1:8000/join');
      const element = driver.findElement(By.id('page-title'));
      element.getText().then(function(text) {
          expect(text).toBe('Join a Room');
      })
      driver.findElement(By.name('roomName')).sendKeys("ABCDEF");
      driver.findElement(By.name('enter')).click()
          .then(() => {
              driver.sleep(1000)
          })
          .then(() => {
              const code = driver.findElement(By.name('code'));
              code.getText().then(function(text) {
                  expect(text).toBe('ABCDEF');
              });
              driver.findElement(By.name('leave')).click()
                  .then(() => {
                      driver.sleep(1000)
                  })
                  .then(() => {
                      const element = driver.findElement(By.id('page-title'));
                      element.getText().then(function(text) {
                          expect(text).toBe('House Party');
                      })
                  })
          })

  })

    it("Can join a room successfully", () =>{
      driver.get('http://127.0.0.1:8000/join');
      const element = driver.findElement(By.id('page-title'));
      element.getText().then(function(text) {
          expect(text).toBe('Join a Room');
      })
      driver.findElement(By.name('roomName')).sendKeys("ABCDEF");
      driver.findElement(By.name('enter')).click()
          .then(() => {
              driver.sleep(1000)
          })
          .then(() => {
              const code = driver.findElement(By.name('code'));
              code.getText().then(function(text) {
                  expect(text).toBe('ABCDEF');
              });
              driver.findElement(By.name('leave')).click()
                  .then(() => {
                      driver.sleep(1000)
                  })
                  .then(() => {
                      const element = driver.findElement(By.id('page-title'));
                      element.getText().then(function(text) {
                          expect(text).toBe('House Party');
                      })
                  })
          })

  })


  it("Can create a room successfully", () =>{
      driver.get('http://127.0.0.1:8000/create');
      const element = driver.findElement(By.id('page-title'));
      element.getText().then(function(text) {
          expect(text).toBe('Create a Room');
      })
      driver.findElement(By.name('refuseGuestControl')).click();
      driver.findElement(By.name('NumOfVotes')).sendKeys('6');
      driver.findElement(By.name('create')).click()
          .then(() => {
              driver.sleep(1000)
          })
          .then(() => {
              const votes = driver.findElement(By.name('votes'));
              votes.getText().then(function(text) {
                  expect(text).toContain('6');
              });
              const canPause = driver.findElement(By.name('pause'));
              canPause.getText().then(function(text) {
                  expect(text).toBe('false');
              });
              driver.findElement(By.name('leave')).click()
                  .then(() => {
                      driver.sleep(1000)
                  })
                  .then(() => {
                      const element = driver.findElement(By.id('page-title'));
                      element.getText().then(function(text) {
                          expect(text).toBe('House Party');
                      })
                  })
          })

  })


  afterAll(async () => {
    await driver.quit();
  }, 15000);

})





