$(document).ready(function() {
    $(".mdl-checkbox__input:checkbox").change(function() {
        if (this.checked) {
            if ($(this).val() == "lr") {
                console.log("lr checked");
                $(this).parent().after("<div id='" + $(this).val() + "'>" +
                    "<legend><b>Parameters</b></legend> " +
                    /*FIT_INTERCEPT*/
                    "<label for='checkbox-1'>" +
                    "<input type='checkbox' id='fit_intercept'>" +
                    "<span>fit_intercept(optional)</span>" +
                    "</label>" + "<br>" +
                    /*NORMALIZE*/
                    "<label for='checkbox-2'>" +
                    "<input type='checkbox' id='normalize'>" +
                    "<span>normalize(default=false)</span>" +
                    "</label>" + "<br>" +
                    /*COPY_X*/
                    "<label for='checkbox-3'>" +
                    "<input type='checkbox' id='copy_x' checked>" +
                    "<span>copy_X(default=true)</span>" +
                    "</label>" + "<br>" +
                    /*N_JOBS*/
                    "<label>Number of jobs to use for the computation (default 1): </label>" +
                    "<input id='number' type='number' min='-1' max='10' onkeydown='return false' value='1'>" +
                    "</div>");
            }
            if ($(this).val() == "svm") {
                /*kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1*/
                console.log("svm checked");
                $(this).parent().after("<div id='" + $(this).val() + "'>" +
                    "<legend><b>Parameters</b></legend> " +
                    /*C*/
                    "<label>Penalty parameter C of the error term (float)(default 1): </label>" +
                    "<input id='c' type='number' value='1.0' step='any'>" + "<br>" +
                    /*EPSILON*/
                    "<label>Epsilon (float)(default 0.1): </label>" +
                    "<input id='epsilon' type='number' value='0.1' step='any'>" + "<br>" +
                    /*KERNEL*/
                    "<label>Kernel(default 'rbf'): </label>" +
                    "<select id='kernel' name='kernel'>" +
                    "<option value='rbf'>rbf</option>" +
                    "<option value='linear'>linear</option>" +
                    "<option value='poly'>poly</option>" +
                    "<option value='sigmoid'>sigmoid</option>" +
                    " </select>" +
                    "<div id='gammaDIV'>" + "<label>Gamma (float)(default auto): </label>" +
                    "<input id='gamma' type='number' min='1' step='1'>" + "</div>" +
                    /*SHRINKING*/
                    "<label>" +
                    "<input type='checkbox' value='true' id='shrinking' checked>" +
                    "<span>shrinking(optional)(default=true)</span>" +
                    "</label>" + "<br>" +
                    /*TOLERANCE*/
                    "<label>tol (float optional)(default 0.001): </label>" +
                    "<input id='tol' type='number' value='0.001' step='any'>" + "<br>" +
                    /*CACHE_SIZE*/
                    "<label>cache_size (float optional)(default 0.001): </label>" +
                    "<input id='cache_size' type='number' value='0.001' step='any'>" + "<br>" +
                    /*VERBOSE*/
                    "<label>" +
                    "<input type='checkbox' value='true' id='verbose'>" +
                    "<span>shrinking(optional)(default=false)</span>" +
                    "</label>" + "<br>" +
                    /*MAX_ITER*/
                    "<label>Hard limit on iterations within solver (int optional)(default -1): </label>" +
                    "<input id='max_iter' type='number' min='-1' max='10' onkeydown='return false' value='-1'>" +
                    "</div>"
                );
                $("select").change(function() {
                    if ($(this).val() == "poly" || $(this).val() == "rbf" || $(this).val() == "sigmoid") {
                        if (!$("#gamma").length) {
                            $(this).after("<div id='gammaDIV'>" + "<label>Gamma (float)(default auto): </label>" +
                                "<input id='gamma' type='number' min='1' value='auto' step='1'>" + "</div>");
                        }
                        if ($(this).val() == "poly") {
                            $(this).after("<div id='degreeDIV'>" + "<label>Degree (int)(default 3): </label>" +
                                "<input id='degree' type='number' min='1' value='3' step='1'>" + "</div>");
                        }
                        if ($(this).val() == "rbf" || $(this).val() == "sigmoid") {
                            if ("#degreeDIV")
                                $("#degreeDIV").remove();
                        }
                        if ($(this).val() == "poly" || $(this).val() == "sigmoid") {
                            if (!$("#coef0DIV").length) {
                                $(this).after(
                                    "<div id='coef0DIV'>" +
                                    "<label>Coef0 (float)(default 0.): </label>" +
                                    "<input id='coef0' type='number' value='0.0' step='any'>" + "</div>"
                                )
                            }
                        }
                        if ($(this).val() == "rbf") {
                            if ($("#coef0DIV").length) {
                                $("#coef0DIV").remove();
                            }
                        }
                    } else {
                        if ("#gammaDIV".length)
                            $("#gammaDIV").remove();
                        if ("#degreeDIV".length)
                            $("#degreeDIV").remove();
                    }
                });
            }
            if ($(this).val() == "tf") {
                console.log("tf checked");
                $(this).parent().after("<div id='" + $(this).val() + "'>" + $(this).val() + "</div>");
            }
        } else {
            if ($(this).val() == "lr") {
                console.log("lr unchecked");
            }
            if ($(this).val() == "svm") {
                console.log("svm unchecked");
            }
            if ($(this).val() == "tf") {
                console.log("tf unchecked");
            }
            $(this).parent().next().remove();
        }
    });
});