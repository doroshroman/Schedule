$(document).ready(function(){

    let subjects = loadSubjects();

    $('#add-subject').click(() =>{
        let subject = $('<input class="subjects" type="text" name="subject">');
        let subj_type = $('<select name="select"><option value="lec">Lecture</option> \
                        <option value="lab" selected>Practise</option>');
        let hours = $('<input type="number" name="subject_hours"><br><br>');

        $('#subject-container').append(subject,subj_type, hours);

        $(".subjects").autocomplete({
            source: subjects
        });
        
    });

    $('#submit').click(async (event) =>{
        event.preventDefault();
        let groupname = $('#groupname').val().trim();
        let total_hours = $('#total-hours').val().trim();
        let date_from = $('#date-from').val().trim();
        let date_to = $('#date-to').val().trim();
        let inputs = $('#subject-container').find("input, select");
        
        
        let schedule = {
            'groupname': groupname,
            'total_hours': total_hours,
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
        
    });

});