import { API_ENDPOINTS } from "./constants.js";

//** submit data to BE */
const submitData = async (data) => {
    console.log(data.nudgeOption, data.directorateOption, data.districtOption, data.designationOption);
    try {
        const payload = {
            nudge: data.nudgeOption,
            directorate: data.directorateOption,
            district: data.districtOption,
            designation: data.designationOption,
        };
        await axios
            .post(API_ENDPOINTS.STORE_DATA, payload)
            .then((response) => {
                console.log(response);
                $("#submitPopup").modal("hide");
                $("#nudgeOption").val("");
                $("#directorateOption").val([]);
                $("#districtOption").val([]);
                $("#designationOption").val([]);
                console.log("done");
            })
            .catch((error) => {
                console.log(error);
                return false;
            });
    } catch (error) {
        console.error(error);
    }
};

const renderNudges = async (id) => {
    console.log(id);
    try {
        let config = {
            method: "get",
            url: API_ENDPOINTS.GET_NUDGES,
            headers: {},
        };

        axios
            .request(config)
            .then((response) => {
                let optionSelection = "";
                //** render district on dropdown */
                response.data.data.map((district) => {
                    console.log(district);
                    optionSelection = optionSelection + `<option value="${district}">${district}</option>`;
                });
                $("#" + id).html(optionSelection);
            })
            .catch((error) => {
                console.log(error);
            });
    } catch (error) {
        console.error(error);
    }
};

const renderDirectorate = async (data) => {
    console.log(data);
    try {
        let config = {
            method: "get",
            url: API_ENDPOINTS.GET_DIRECTORATE,
            headers: {},
        };

        axios
            .request(config)
            .then((response) => {
                // console.log(JSON.stringify(response.data));
                let optionSelection = "";
                //** render district on dropdown */
                response.data.data.map((district) => {
                    console.log(district);
                    optionSelection = optionSelection + `<option value="${district}">${district}</option>`;
                });
                $("#directorateOption").html(optionSelection);
                $('#directorateOption').multiselect('reload');
            })
            .catch((error) => {
                console.log(error);
            });
    } catch (error) {
        console.error(error);
    }
};

const _parseData = async (dataList) => {
    let dataStr = "";
    //** concat the selected values to pass in the urls */
    for (const data of dataList) {
        dataStr += `${data},`;
    }
    console.log(dataStr);
    dataStr = dataStr.substring(0, dataStr.length - 1); // remove the last ,
    return dataStr;
};

const renderDesignations = async (data) => {
    console.log("renderDesignations");
    console.log(data);
    try {
        //** concat the selected values to pass in the urls */
        const directorateStr = await _parseData(data.directorate);

        let config = {
            method: "get",
            url: `${API_ENDPOINTS.GET_DESIGNATION_BY_DIRECTORATE}?directorate=${encodeURIComponent(directorateStr)}`,
            headers: {},
        };

        axios
            .request(config)
            .then((response) => {
                console.log("renderDesignations response ->");
                console.log(JSON.stringify(response.data));
                let optionSelection = "";
                //** render district on dropdown */
                response.data.data.map((designation) => {
                    console.log(designation);
                    optionSelection = optionSelection + `<option value="${designation}">${designation}</option>`;
                });
                $("#designationOption").html(optionSelection);
                $('#designationOption').multiselect('reload');
                $("#districtOption").val([]);
                $('#districtOption').multiselect('reload');
                
            })
            .catch((error) => {
                console.log(error);
            });
    } catch (error) {
        console.error(error);
    }
};

const renderDistricts = async (data) => {
    console.log(data);
    try {
        //** concat the selected values to pass in the urls */
        const directorateStr = await _parseData(data.directorate);

        //** concat the selected values to pass in the urls */
        const designationsStr = await _parseData(data.designation);

        let config = {
            method: "get",
            url: `${API_ENDPOINTS.GET_DISTRICT_BY_DIRECTORATE_AND_DESIGNATION}?directorate=${encodeURIComponent(
                directorateStr
            )}&designation=${encodeURIComponent(designationsStr)}`,
            headers: {},
        };

        axios
            .request(config)
            .then((response) => {
                // console.log(JSON.stringify(response.data));
                let optionSelection = "";
                //** render district on dropdown */
                response.data.data.map((district) => {
                    console.log(district);
                    optionSelection = optionSelection + `<option value="${district}">${district}</option>`;
                });
                $("#districtOption").html(optionSelection);
                $('#districtOption').multiselect('reload');
            })
            .catch((error) => {
                console.log(error);
            });
    } catch (error) {
        console.error(error);
    }
};

//** submit data to BE */
const sentMessageSingle = async (data) => {
    console.log(data);
    try {
        const payload = {
            mobile: data.mobile,
            nudge: data.nudge,
        };
        await axios
            .post(API_ENDPOINTS.SENT_MSG_SINGLE, payload)
            .then((response) => {
                console.log(response);

                if (response.data.status_code == 500) {
                    console.log("failed 500");
                    showToast("failed"); //popup for response
                    return false;
                }

                // alert("Data submitted succesfully");
                $("#submitPopupSingle").modal("hide");
                $("#mobile-input").val("");

                showToast("success"); //popup for response
            })
            .catch((error) => {
                console.log(error);
                showToast("failed"); //popup for response
                return false;
            });
    } catch (error) {
        console.error(error);
    }
};

const sentMessageBulk = async (data) => {
    console.log(data.nudgeOption, data.directorateOption, data.districtOption, data.designationOption);
    try {
        //** concat the selected values to pass in the urls */
        const directorateStr = await _parseData(data.directorateOption);

        //** concat the selected values to pass in the urls */
        const designationsStr = await _parseData(data.designationOption);

        //** concat the selected values to pass in the urls */
        const districtStr = await _parseData(data.districtOption);

        const payload = {
            nudge: data.nudgeOption,
            directorate: directorateStr,
            district: districtStr,
            designation: designationsStr,
        };
        await axios
            .post(API_ENDPOINTS.SENT_MSG_BULK, payload)
            .then((response) => {
                console.log(response);

                if (response.data.status_code == 500) {
                    console.log("failed 500");
                    showToast("failed"); //popup for response
                    return false;
                }

                $("#submitPopup").modal("hide");
                $("#nudgeOption").val("");
                $("#directorateOption").val([]);
                $("#districtOption").val([]);
                $("#designationOption").val([]);
                $('#directorateOption').multiselect('reload');
                $('#districtOption').multiselect('reload');
                $('#designationOption').multiselect('reload');
                showToast("success"); //popup for response
            })
            .catch((error) => {
                showToast("failed"); //popup for response
                console.log(error);
                return false;
            });
    } catch (error) {
        console.error(error);
    }
};

const showToast = (status) => {
    $(".toast").removeClass("hide");
    $(".toast").addClass("show");
    setTimeout(() => {
        $(".toast").removeClass("show");
        $(".toast").addClass("hide");
    }, 5000);

    if (status == "success") {
        $(".toast .toast-body").text("Message sent successfully");
        $(".toast").addClass("bg-primary");
        $(".toast").removeClass("bg-danger");
    } else {
        $(".toast .toast-body").text("Message sent failed");
        $(".toast").removeClass("bg-primary");
        $(".toast").addClass("bg-danger");
    }
};

export {
    submitData,
    renderDistricts,
    renderDesignations,
    sentMessageSingle,
    sentMessageBulk,
    renderNudges,
    renderDirectorate,
};
