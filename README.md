# swasti-framework

Prototype for Voice enabled web services for space weather forecasting

url: [https://swasti-framework.azurewebsites.net/](https://swasti-framework.azurewebsites.net/)

- Data only present for January 2022

Routes

```
GET /get_obs?param=<paramvalue>
Header: paramvalue should consist date on which obs requested
Returns: {
    temp: [array],
    density: [array],
    velocity: [array]
}
```

```
GET /avgvelocity/?text=<paramvalue>
Header: paramvalue should consist date on which obs requested
Returns: {
    avg_den:val,
    avg_temp:val,
    date:string,
    url:string, url for spoken response,
    val:string, avg velocity val
}
```
