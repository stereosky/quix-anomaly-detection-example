```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
rawdata{{ fa:fa-arrow-right-arrow-left rawdata &#8205}}:::topic --> influxdb_raw_sink[fa:fa-rocket influxdb_raw_sink &#8205];
mqtt_source[fa:fa-rocket mqtt_source &#8205] --> rawdata{{ fa:fa-arrow-right-arrow-left rawdata &#8205}}:::topic;


classDef default font-size:110%;
classDef topic font-size:80%;
classDef topic fill:#3E89B3;
classDef topic stroke:#3E89B3;
classDef topic color:white;
```