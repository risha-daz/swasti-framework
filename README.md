# swasti-framework

Prototype for Voice enabled web services for space weather forecasting

url: [https://swasti-framework.azurewebsites.net/](https://swasti-framework.azurewebsites.net/)

```GET /get_obs?param=<paramvalue>
Header: paramvalue should consist date on which obs requested
Returns: {
    temp: [array],
    density: [array],

}
```
