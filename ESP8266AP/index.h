const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE html>
  <html>
    <style>
      body{
        background-color: #FAFAFA;
      }
      table, th, td{
        border:1px solid black;
      }
      .card{
        max-width: 960px;
        min-height: 540px;
        background: #0080ff;
        padding: 30px;
        box-sizing: border-box;
        color: #FFF;
        margin:20px;
        box-shadow: 0px 2px 18px -4px rgba(0,0,0,0.75);
      }
      .barcontainerV{
        background-color: #181818;
        position: relative;
        width: 50px;
        height: 320px;
        display: inline-block;
        margin-top: 4px;
      }
      .barV{
        background-color: #17ff59;
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 0%;
        box-sizing: border-box;
        transform-origin: bottom;
      }
      .GYROcircle{
        height: 180px;
        width: 180px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        position: relative;
        margin-top: 4px;
      }
      .GYROdot{
        height: 20px;
        width: 20px;
        background-color: #FF0000;
        position: absolute;
        top: 80px;
        left: 80px;
        border-radius: 50%;
        display: inline-block;
        text-align: center;
      }
    </style>
    <body>
      <div class="card">
        <!-- text displayed in the card -->
        <h4>Update web page without refresh</h4>
        <h4 id="rawDataStr">raw data string</h4>
        <table>
          <!-- data table -->
          <tr>
            <!-- data titles -->
            <th style="width:10%">Exhaust Temperature (C)</th>
            <th style="width:10%">Engine (RPM)</th>
            <th style="width:10%">Throttle (%)</th>
            <th style="width:10%">Intake Temperature (C)</th>
            <th style="width:10%">Coolant Temperature (C)</th>
          </tr>
          <tr style="text-align:right">
            <!-- data values -->
            <td><span id="data20">0</span></td>
            <td><span id="data30">0</span></td>
            <td><span id="data50">0</span></td>
            <td><span id="data60">0</span></td>
            <td><span id="data70">0</span></td>
          </tr>
          <tr>
            <!-- data visulize -->
            <td style="text-align:center">
              <div class="barcontainerV">
                <div class="barV" id="barExTemp">
                </div>
              </div>
            </td>
            <td style="text-align:center">
              <div class="barcontainerV">
                <div class="barV" id="barEngRPM">
                </div>
              </div>
            </td>
            
            <td style="text-align:center">
              <div class="barcontainerV">
                <div class="barV" id="barThro">
                </div>
              </div>
            </td>
            <td style="text-align:center">
              <div class="barcontainerV">
                <div class="barV" id="barInTemp">
                </div>
              </div>
            </td>
            <td style="text-align:center">
              <div class="barcontainerV">
                <div class="barV" id="barCoTemp">
                </div>
              </div>
            </td>
          </tr>
        </table>
        
        <!--table for extra data w/o visulization-->
        <br />
        <table width="100%">
        <tr>
        <th colspan="3">GYR</th>
        <th colspan="3">ACC</th>
        </tr>
        <tr>
            <td>a</td>
            <td>a</td>
            <td>a</td>
            <td>a</td>
            <td>a</td>
            <td>a</td>
        </tr>
        </table>
        
      </div>
      <script>
        // JavaScript
        // set refresh rate in Hz
        var refreshRate_Hz = 10;
        // Call this function repetatively with time interval in ms
        setInterval(function() { getData(); }, 1000/refreshRate_Hz);
        // get data from ESP
        function getData() {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (true) {
              // actual code:         this.readyState == 4 && this.status == 200
              // test code:           true
              const rawDataStr = "10,20,30|40,50,60|1000|3000|70|80|25|30|20|";
              // actual code:         this.responseText
              // test code:           "10,20,30|40,50,60|500|3000|70|80|25|30|20|"
              // current data receiving w/ format:
                // ACCX,ACCY,ACCZ|GYRX,GYRY,GYRZ|A1|engineSpeed(RPM)|engineLoad(%)|throttle(%)|intakeTemp(C)|coolantTemp(C)|currentTime(ms)|
              document.getElementById("rawDataStr").innerHTML = rawDataStr;
              processData(rawDataStr);
              window.AppInventor.setWebViewString("" + this.responseText);  // RESPUESTA A CadenaDeWebView
            }
          };
          xhttp.open("GET", "readADC", true);
          xhttp.send();
        }
        function processData(allDataStr) {
          const dataValues = [];
          var n0 = 0;
          var singleDataStr = "";
          for(var i = 0;i < allDataStr.length;i++) {
            if(allDataStr[i] != '|') {
              singleDataStr += allDataStr[i];
            }
            else {
              var n1 = 0;
              const subDataValues = [];
              var singleSubDataStr = "";
              for(var j = 0;j < singleDataStr.length;j++) {
                if(singleDataStr[j] != ','){
                    singleSubDataStr += singleDataStr[j];
                }
                else{
                    subDataValues[n1]=singleSubDataStr;
                    n1++;
                    singleSubDataStr="";
                }
              }
              subDataValues[n1]=singleSubDataStr;
              dataValues[n0] = subDataValues;
              n0++;
              singleDataStr = "";
            }
          }
          dataValues[2][0] = ((parseInt(dataValues[2][0]) * 3.3 / 1024 * 5 / 3.2 - 1.25)/0.005).toFixed(0).toString();
          
          for(var i=0;i<n0;i++){
            for(var j=0;j<dataValues[i].length;j++){
              var element = document.getElementById("data"+i.toString()+j.toString());
              if(element){
                element.innerHTML = dataValues[i][j];
              }
            }
            
          }
          
          //engine RPM max: 13,000
          var enginePercent = (parseFloat(dataValues[3])/13000*100).toString();
          //throttle visulize
          document.getElementById("barEngRPM").style.height = enginePercent+"%";
        }
      </script>
    </body>
  </html>
)=====";
