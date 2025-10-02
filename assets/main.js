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

    function setQS_palette(newval, colorParam) {
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

    function setParam1(value) {
        var param1 = document.getElementById('param1');
        param1.value = value;
    }

    function setParam2(value) {
        var param2 = document.getElementById('param2');
        param2.value = value;
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
        var isComplete = false;

        var saveFilename = $("#sacred-guid-value").val();

        if (typeof apiURL == "undefined") {
            var socode = document.getElementById('sacred-output-code');
            socode.innerHTML = "Text output: No image data to display";

            return;
        }

        $("#time-elapsed").removeClass("not-loaded");
        $("#time-elapsed").removeClass("loaded");

        var daInterval = setInterval(()=> {
            const end = performance.now();
                
            if (!isComplete) {
                $("#time-elapsed").html(`${(end - start) / 1000.0}s`);
                $("#time-elapsed").addClass("not-loaded");
            } else {
                window.clearTimeout(daInterval);
            }
        }, 500);
   
        var resp = $.getJSON(apiURL)
            .done(function( data ) {
                var socode = document.getElementById('sacred-output-code');

                var outputImg = document.getElementById('output-img');
                outputImg.src = 'data:image/png;base64,' + data.image;

                var saveImgBtn = document.getElementById('sacred-image-dl');
                saveImgBtn.href = 'data:image/png;base64,' + data.image;
                saveImgBtn.download = saveFilename;

                var sacred_output = document.getElementById('sacred-output');                

                data.image = "";
                socode.innerHTML = JSON.stringify(data, null, 2);

                let paletteData = data['palette'];
                let rnd_palette_chosen = data['rnd_palette_name'];

                let tableRef = document.getElementById("palette-table");
                let caption = document.getElementById("palette-caption");
                caption.innerText = rnd_palette_chosen;
  
                let newRow = tableRef.insertRow(-1);

                var soph_text_content = "[";

                for (var ic = 0; ic < paletteData.length; ic++) {
                    var icItem = paletteData[ic];

                    let newCell = newRow.insertCell(-1);
                    newCell.style.backgroundColor = icItem;
                    newCell.style.color = getForegroundColor(icItem);
                    
                    let newText = document.createTextNode(icItem);
                    newCell.appendChild(newText);

                    soph_text_content += "\"" + icItem + "\"";

                    if (ic < paletteData.length - 1) {
                        soph_text_content += ",";
                    }
                }

                soph_text_content += "]";

                var soph = document.getElementById("sacred-palette-hex");
                var sophtext = document.createTextNode(soph_text_content);
                soph.appendChild(sophtext);

                var thisItemDiv = document.createElement("div");
                thisItemDiv.setAttribute("id", "exif-url-0");
                thisItemDiv.setAttribute("class", "exif-url");

                sacred_output.appendChild(thisItemDiv); 

                var alreadyDone = [];
                
                window.__nates_shit = [];

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

                            window.__nates_shit.push(data);

                            if (data.errors.length > 0 || data.exif != "{}") {
                                var textNode = document.createTextNode(xxzzvv);
                                moonColony.appendChild(textNode);
                                spaceDebris.appendChild(moonColony);
                                thisItemDiv.appendChild(spaceDebris);
                            }
                        })
                        .fail((f) => {
                            var textNode = document.createTextNode("No data");
                            thisItemDiv.appendChild(textNode)
                        });
                    }
                }
            })
            .fail((e) => {
                console.log( "callAPI getJSON error fail" );
            })
            .always((e) => {
                const end = performance.now();
                isComplete = true;
                $("#time-elapsed").removeClass("not-loaded");
                
                $("#time-elapsed").html(`${(end - start) / 1000.0}s`);

                hljs.highlightAll();

                $("#result-container-img").addClass("loaded");
                $("#output-img").addClass("loaded");
                $("#time-elapsed").addClass("loaded");
            });

        return resp;
    }

    function getForegroundColor(backgroundColor) {
        // 1. Convert the background color (e.g., "#RRGGBB" or "rgb(r,g,b)") to an RGB array.
        // This example assumes a hex string input for simplicity.
        let r = parseInt(backgroundColor.substring(1, 3), 16);
        let g = parseInt(backgroundColor.substring(3, 5), 16);
        let b = parseInt(backgroundColor.substring(5, 7), 16);

        // 2. Convert sRGB to linear RGB.
        // Apply gamma correction for each color component.
        function sRGBtoLinear(c) {
            c /= 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        }

        let rLinear = sRGBtoLinear(r);
        let gLinear = sRGBtoLinear(g);
        let bLinear = sRGBtoLinear(b);

        // 3. Calculate relative luminance (L).
        // Using the ITU-R BT.709 standard.
        const luminance = 0.2126 * rLinear + 0.7152 * gLinear + 0.0722 * bLinear;

        // 4. Determine foreground color based on luminance.
        // A common threshold is around 0.179 (derived from contrast ratio calculation).
        // If luminance is high, use black; otherwise, use white.
        if (luminance > 0.179) {
            return "#000000"; // Black
        } else {
            return "#FFFFFF"; // White
        }
    }

    function goClicked() {
        var params = getQueryParameters();

        var param1 = document.getElementById('param1').value;
        var param2 = document.getElementById('param2').value;
        var compfunc = document.getElementById('compfunc').value;
        var paramfont = document.getElementById('paramfont').value;
        var paramInsertSource = document.getElementById('insertSource').value;        
        var paramImage = document.getElementById('img-upload');
        var param3 = document.getElementById('param3').value;
        var paramFloodBoxes = document.getElementById('floodBoxes').checked;
        var param4 = document.getElementById('param4').checked;
        var paramBuckyBits = document.getElementById('buckyBits').value;

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
        params["param4"] = param4;
        params["buckyBits"] = paramBuckyBits;

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

    function bottomFunction() {
        var sidebar = document.getElementById("sidebar");
        sidebar.scrollTop = sidebar.scrollHeight;
    } 

    function scrollBelowImage() {
        var sacred_output = document.getElementById("sacred-output");
        sacred_output.scrollIntoView();
    }

    function copyToClipboard() {        
        var copyText = document.getElementById("sacred-guid-value");

        copyText.select();
        copyText.setSelectionRange(0, 99999); // For mobile devices
        navigator.clipboard.writeText(copyText.value);
        console.log("Copied to clipboard: " + copyText.value);
    } 

    function toggleEss() {
        $(".tdl-normal").toggleClass('hidden');
        $(".tdl_sep").toggleClass('hidden');
    }
    
    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
    });    

    document.fonts.ready.then(function () {
        document.getElementById("main-hex").style.opacity = '1';
    });

    // 1) Style each dropdown choice to match its option
    function decorateChoices() {
        const paletteSel = document.getElementById('palette');
        // map <option> -> rendered .choices__item[data-value="..."]
        [...paletteSel.options].forEach(opt => {
            const val = (opt.value || '').toString();
            const key = (opt.dataset.key || val).toLowerCase().trim();
            const color = opt.dataset.color || '';

            const choiceEl = choice.dropdown.element.querySelector(
            `.choices__item[data-value="${CSS.escape(val)}"]`
            );
            if (!choiceEl) return;

            choiceEl.classList.add(PREFIX + key);
            if (color) choiceEl.style.setProperty('--chip', color);
        });
    }

    // 2) Keep the <select> capsule styled by current selection
    function syncSelectClass() {
        const paletteSel = document.getElementById('palette');

        paletteSel.classList.add(`palette-numba-${paletteSel.value}`);

        // also mirror the class on the visible single item (belt & suspenders)
        const single = paletteSel.querySelector('.choices__list--single .choices__item');

        if (single) {
            [...single.classList].forEach(c => {
                if (c.startsWith('palette-numba-')) single.classList.remove(c);
            });
            single.classList.add(`palette-numba-${paletteSel.value}`);
        }
    } 

    function adjustParam(id, delta, valueIfEmpty=false) {
        const param1 = document.getElementById(id);

        let val = parseInt(param1.value, 10);
        
        if (isNaN(val)) {           
            if(valueIfEmpty !== false) {
                param1.value = valueIfEmpty;
                param1.dispatchEvent(new Event('input', { bubbles: true }));
            }
            return;
        }

        val += delta;
        param1.value = val.toString();

        // fire input event in case anything else is listening
        param1.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function clearParam(id) {
        const paramControl = document.getElementById(id);

        if (paramControl) {
            paramControl.value = "";
        }
    }

    const palette = document.getElementById('palette');
    const PREFIX = 'palette-numba-';
    const paletteSel = document.getElementById('palette');

    var choice = "";
    var buckyLabels = [];
    
    $( document ).ready(function() {
        $.getJSON("/buckybits")
        .done(function( data ) {
            buckyLabels = data;
        
            choice = new Choices('#palette', {
                searchEnabled: true,
                searchChoices: true,
                shouldSort: false,
                allowHTML: true,
                searchFields: [
                    'label',
                    'value',
                    'customProperties.band',
                    'customProperties.tags'
                ],
                searchResultLimit: 100
            });

            callAPI();

            decorateChoices();
            syncSelectClass();
            choice.passedElement.element.addEventListener('change', syncSelectClass);
            choice.dropdown.element.addEventListener('showDropdown', decorateChoices);

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

            var palette = document.getElementById("palette");

            // add a class to every <option> based on its value (or data-key, if you prefer)
            [...palette.options].forEach(opt => {
            const key = (opt.dataset.key || opt.value || '')
                .toString().trim().toLowerCase();
            if (key) opt.classList.add(PREFIX + key);
            });

            // keep the <select> class in sync with the current selection
            function applySelectClass() {
            // remove any previous prefixed class
            [...palette.classList].forEach(c => {
                if (c.startsWith(PREFIX)) palette.classList.remove(c);
            });
            // add the new one
            const key = (palette.selectedOptions[0]?.dataset.key || palette.value || '')
                .toString().trim().toLowerCase();
            if (key) palette.classList.add(PREFIX + key);
            }

            applySelectClass();
            palette.addEventListener('change', applySelectClass);

            const buckyInput = document.getElementById("buckyBits");        
            
            function updateCheckboxesFromNumber() {
                let value = parseInt(buckyInput.value) || 0;
                for (let i = 0; i < buckyLabels.length; i++) {
                    document.getElementById("bit" + i).checked = (value >> i) & 1;
                }
            }

            function updateNumberFromCheckboxes() {
                let value = 0;
                for (let i = 0; i < buckyLabels.length; i++) {
                    if (document.getElementById("bit" + i).checked) {
                        value |= (1 << i);
                    }
                }
                buckyInput.value = value;
            }

            // Events
            buckyInput.addEventListener("input", updateCheckboxesFromNumber);

            for (let i = 0; i < buckyLabels.length; i++) {
                document.getElementById("bit" + i).addEventListener("change", updateNumberFromCheckboxes);
            }

            updateCheckboxesFromNumber();

            document.getElementById('param1-decr').addEventListener('click', () => adjustParam('param1', -1, 0));
            document.getElementById('param1-incr').addEventListener('click', () => adjustParam('param1', 1, 0));
            document.getElementById('param1-clear').addEventListener('click', () => clearParam('param1'));

            document.getElementById('param2-decr').addEventListener('click', () => adjustParam('param2', -1, 0));
            document.getElementById('param2-incr').addEventListener('click', () => adjustParam('param2', 1, 0));
            document.getElementById('param2-clear').addEventListener('click', () => clearParam('param2'));

            document.getElementById('variant-decr').addEventListener('click', () => adjustParam('param3', -1, 0));
            document.getElementById('variant-incr').addEventListener('click', () => adjustParam('param3', 1, 0));
            document.getElementById('variant-clear').addEventListener('click', () => clearParam('param3'));
        });
    }); 
    
    $( window ).on( "load", function() {
        console.log("window is loaded");
    });

    $(document).on('mousemove', function(e) {
        var hhh = $('#myBtn').height();
        var iii = $('#myBtn2').height();

        $('#myBtn').css('top', e.clientY - (hhh / 2));
        $('#myBtn2').css('top', e.clientY - (iii / 2));
    });

    $(document).keypress(function (e) {
        if (e.keyCode === 13) {
            $("#btnGo").click();
        }
    });