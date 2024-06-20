    function generateUUID(){
        var d = new Date().getTime();
        if(window.performance && typeof window.performance.now === "function"){
            d += performance.now(); //use high-precision timer if available
        }
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (d + Math.random()*16)%16 | 0;
            d = Math.floor(d/16);
            return (c=='x' ? r : (r&0x3|0x8)).toString(16);
        });
        return uuid;
    }

    function guidclick() {
        var uuid = generateUUID();       
        $("#myguid").val(uuid);
    }

    function getQueryParameters() {
      var queryString = location.search.slice(1),
          params = {};

      queryString.replace(/([^=]*)=([^&]*)&*/g, function (_, key, value) {
        params[key] = value;
      });

      return params;
    }
    
    function setQueryParameters(params) {
      var query = [],
          key, value;

      for(key in params) {
        if(!params.hasOwnProperty(key)) continue;
        value = params[key];
        query.push(key + "=" + value);
      }

      location.search = query.join("&");
    }

    function setQS_imageop(newval) {
        var params = getQueryParameters();

        if(params.imageop != newval) {
          params.imageop = newval;
          setQueryParameters(params);
        }
    }

    function setQS_palette(newval) {
        var params = getQueryParameters();

        if(params.palette != newval) {
          params.palette = newval;
          setQueryParameters(params);
        }
    }

    function setQS(key, val) {
        var params = getQueryParameters();

        if(params[key] != val) {
          params[key] = val;
          setQueryParameters(params);
        }
    }

    function downloadBase64File(contentType, base64Data, fileName) {
        const linkSource = `data:${contentType};base64,${base64Data}`;
        const downloadLink = document.createElement("a");
        downloadLink.href = linkSource;
        downloadLink.download = fileName;
        downloadLink.click();
    }
   
    function callAPI() {
        const start = performance.now();        
        var saveFilename = $("#sacred-guid-value").val();

        if (typeof apiURL == "undefined") {
            return;
        }

        var resp = $.getJSON(apiURL)
            .done(function( data ) {
                var outputImg = document.getElementById('output-img');
                outputImg.src = 'data:image/png;base64,' + data.image;

                var saveImgBtn = document.getElementById('sacred-image-dl');
                saveImgBtn.href = 'data:image/png;base64,' + data.image;
                saveImgBtn.download = saveFilename;

                var sacred_output = document.getElementById('sacred-output');
                var socode = document.getElementById('sacred-output-code');

                // var soPalette = document.getElementById('sacred-output-palette');

                data.image = "";
                socode.innerHTML = JSON.stringify(data, null, 2);

                let paletteData = data['palette'];

                let tableRef = document.getElementById("palette-table");
  
                let newRow = tableRef.insertRow(-1);

                for (var ic = 0; ic < paletteData.length; ic++) {
                    var icItem = paletteData[ic];

                    let newCell = newRow.insertCell(-1);
                    newCell.style.backgroundColor = icItem
                    
                    let newText = document.createTextNode("");
                    newCell.appendChild(newText);
                }

                var thisItemDiv = document.createElement("div");
                thisItemDiv.setAttribute("id", "exif-url-0");
                thisItemDiv.setAttribute("class", "exif-url");

                sacred_output.appendChild(thisItemDiv); 

                var alreadyDone = [];

                for (var insertI in data.inserts_used) {                    
                    var item = data.inserts_used[insertI];

                    if (alreadyDone.indexOf(item) < 0) {
                        alreadyDone.push(item);

                        var asdfasdf = $.get("/exif" + item)
                        .done((data) => {
                            var spaceDebris = document.createElement("pre");
                            var moonColony = document.createElement("code");

                            moonColony.setAttribute("class", "language-json");                            

                            var xxzzvv = JSON.stringify(data, undefined, 2);

                            var textNode = document.createTextNode(xxzzvv);
                            moonColony.appendChild(textNode);
                            spaceDebris.appendChild(moonColony);
                            thisItemDiv.appendChild(spaceDebris);
                        })
                        .fail((f) => {
                            var textNode = document.createTextNode("No data");
                            thisItemDiv.appendChild(textNode)
                        });
                    }
                }
            })
            .always((e) => {
                const end = performance.now();
                
                $("#time-elapsed").html(`${(end - start) / 1000.0}s`);

                hljs.highlightAll();

                $("#result-container-img").addClass("loaded");
                $("#output-img").addClass("loaded");
            });

        return resp;
    }

    function goClicked() {
        var params = getQueryParameters();

        var param1 = document.getElementById('param1').value;
        var param2 = document.getElementById('param2').value;
        var compfunc = document.getElementById('compfunc').value;
        var paramfont = document.getElementById('paramfont').value;
        var paramInsertSource = document.getElementById('insertSource').value;
        var paramFloodBoxes = document.getElementById('floodBoxes').checked;
        var paramImage = document.getElementById('img-upload');
        var param3 = document.getElementById('param3').value;

        console.dir(paramImage);

        var query = [];
        var key;
        var value;

        params["param1"] = param1;
        params["param2"] = param2;
        params["param3"] = param3;
        params["compfunc"] = compfunc;
        params["paramfont"] = paramfont;
        params["insertSource"] = paramInsertSource;
        params["floodBoxes"] = paramFloodBoxes;

        for (key in params) {
            if(!params.hasOwnProperty(key)) continue;
            value = params[key];

            if (value && value !== "") {
                query.push(key + "=" + value);
            }
        }

        location.search = query.join("&");
    }

    function topFunction() {
        document.getElementById("sidebar").scrollTop = 0;        
    } 

    function copyToClipboard() {        
        var copyText = document.getElementById("sacred-guid-value");

        copyText.select();
        copyText.setSelectionRange(0, 99999); // For mobile devices
        navigator.clipboard.writeText(copyText.value);
        console.log("Copied to clipboard: " + copyText.value);
    } 
    
    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
    });    

    // tags: document.ready
    $( document ).ready(function() {
        callAPI();

        var imgUpload = document.getElementById("img-upload");

        imgUpload.addEventListener("change", () => {
            if (imgUpload.files.length == 1) {
                var prom = toBase64(imgUpload.files[0]);

                prom.then((e) => {
                    var resp = $.post("/processing", {"image":e})
                    .done(function( data ) {
                        console.dir(data);
                    });
                });                
            }
          });
    });
 
    $( window ).on( "load", function() {
        
    });

    $(document).on('mousemove', function(e) {
        var hhh = $('#myBtn').height();
        $('#myBtn').css('top', e.clientY - (hhh / 2));
    });