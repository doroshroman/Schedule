$(document).ready(function(){

    let subjects = loadSubjects();

    $('#add-subject').click(() =>{
        let subject = '<div class="form-group col-md-4"> \
                        <span>Subject</span> \
                        <input class="subjects form-control" type="text" name="subject"></div>';

        let subj_type = '<div class="form-group col-md-4"> \
                        <span>Type</span> \
                        <select name="select"><option value="lec">Lecture</option> \
                        <option value="lab" selected>Practise</option></div>';

        let hours = '<div class="form-group col-md-2">\
                    <span>Hours</span> \
                    <input type="number" class="form-control" name="subject_hours"><br></div>';

        $('#subject-container').append(subject,subj_type, hours);

        $(".subjects").autocomplete({
            source: subjects
        });
        
    });
    // Validation here
    $("#semester-form").validate({
        rules: {
            groupname: "required",
            subject: "required",
            subject_hours: "required"
        },
        messages: {
            groupname: "Please enter group name",
            subject: "Please enter subject",
            subject_hours: "Please enter valid hours"
        },
        submitHandler: function(form, event) { 
            //event.preventDefault();
            sendToServer();
            return false;
        }
    });
    async function sendToServer(){
        
        let groupname = $('#groupname').val().trim();
        let date_from = $('#date-from').val().trim();
        let date_to = $('#date-to').val().trim();
        let inputs = $('#subject-container').find("input, select");
        
        
        let schedule = {
            'groupname': groupname,
            'date_from': date_from,
            'date_to': date_to
        };
        
        let subjects = [];
        for(let i = 0;i < inputs.length;i += 3){
            let subject = inputs[i].value.trim();
            let subj_type = inputs[i + 1].value.trim();
            let hours = inputs[i + 2].value.trim(); 
            subjects.push({
                'subject' : subject,
                'subj_type': subj_type,
                'hours' : hours
            });
            
        }
        schedule['subjects'] = subjects;
        
        // Send to server
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(schedule)
        }

        const response = await fetch('/create', options);
        const content_type = response.headers.get('Content-Type');
        if (content_type.search('json') != -1){
            const data = await response.json();
            $('#flash').show().text(data['flash'])
        }else{
            $('#flash').hide()
        }
        

    }

});