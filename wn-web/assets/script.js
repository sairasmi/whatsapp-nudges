import {
    renderDistricts,
    renderDesignations,
    sentMessageSingle,
    sentMessageBulk,
    renderNudges,
    renderDirectorate,
} from "./get_data.js";

$(document).ready(async () => {
    await ready();

    $("#bulk-tab-id").click(function () {
        $("#bulk-tab-content-id").show();
        $("#single-tab-content-id").hide();

        $("#single-tab-id").removeClass("active");
        $("#bulk-tab-id").addClass("active");
    });

    $("#single-tab-id").click(function () {
        $("#single-tab-content-id").show();
        $("#bulk-tab-content-id").hide();

        $("#single-tab-id").addClass("active");
        $("#bulk-tab-id").removeClass("active");

        renderNudges("nudgeOption2");
    });

    $("#submit-nudge-bulk").click(function () {
        let nudgeOption = $("#nudgeOption").val();
        let directorateOption = $("#directorateOption").val();
        let districtOption = $("#districtOption").val();
        let designationOption = $("#designationOption").val();

        nudgeOption = nudgeOption == "" ? null : nudgeOption;
        directorateOption = directorateOption.length == 0 ? null : directorateOption;
        districtOption = districtOption.length == 0 ? null : districtOption;
        designationOption = designationOption.length == 0 ? null : designationOption;

        if (nudgeOption && directorateOption && districtOption && designationOption) {
            const res1 = sentMessageBulk({ nudgeOption, directorateOption, districtOption, designationOption });
            console.log(res1);
        } else {
            alert("Please select all the options to send the nudge");
        }
    });

    $("#submit-nudge-single").click(function () {
        let nudge = $("#nudgeOption2").val();
        let mobile = $("#mobile-input").val();

        if (mobile && nudgeOption) {
            const res1 = sentMessageSingle({ mobile, nudge });
            console.log(res1);
        } else {
            alert("Please enter nudge and mobile number");
        }
    });

    $("#directorateOption").change(function () {
        const payload = { directorate: $(this).val() };
        renderDesignations(payload);
    });

    $("#designationOption").change(function () {
        const directorate = $("#directorateOption").val();
        console.log("directorate", directorate);
        const payload = { directorate, designation: $(this).val() };
        renderDistricts(payload);
    });
});

const ready = async () => {
    console.log("ready");
    $('#directorateOption').multiselect({
        columns: 1,
        placeholder: 'Select Directorate',
        search: true,
        selectAll: true
    });
    $('#designationOption').multiselect({
        columns: 1,
        placeholder: 'Select Designation',
        search: true,
        selectAll: true
    });
    $('#districtOption').multiselect({
        columns: 1,
        placeholder: 'Select District',
        search: true,
        selectAll: true
    });
    await renderNudges("nudgeOption");
    await renderDirectorate();
};
