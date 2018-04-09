class FormController {

  constructor() {}



}

class FieldLoader {

  constructor() {}

}





function loadConfigCCData() {

    var slider_value = slider.noUiSlider.get();

    return {
        configname: document.getElementById("configname").value,
        rangevalue_lower: slider_value[0],
        rangevalue_upper: slider_value[1],
        num_males: document.getElementById("num-males").value,
        num_females: document.getElementById("num-females").value,
        num_cap: document.getElementById("num-cap").value,
        num_170: document.getElementById("num-170").value,
        num_naz: document.getElementById("num-naz").value,
        num_x_naz: document.getElementById("num-x-naz").value
    };

}

function loadAndSendConfigCCData() {
    $.post("utils/uploadconfig.php", loadConfigCCData(), callbackOnSendConfigCCDataFinished);
}

function callbackOnSendConfigCCDataFinished(response, status) {
    response = JSON.parse(JSON.stringify(eval("(" + response + ")")));
    console.log(response);
    if (response.querystatus === "Good") {
        M.toast({
            html: 'Configurazione inserita con successo!',
            classes: 'rounded'
        });
    }
    if (response.querystatus === "Bad") {
        M.toast({
            html: 'Impossibile inserire record causa nomi in conflitto o campi vuoti!',
            classes: 'rounded'
        });
    }
}
