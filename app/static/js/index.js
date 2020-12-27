function loadSubjects(){
    let subjects = [];
    $.getJSON('/subjects', function(data, status, xhr){
    }).done(function(data){
        for (let i = 0; i < data.length; i++ ) {
            subjects.push(data[i].title);
        }
    });
    return subjects;
}
function loadGroups(){
    let groups = [];
    $.getJSON('/groups', function(data, status, xhr){
    }).done(function(data) {
        for (let i = 0; i < data.length; i++ ) {
            groups.push(data[i].name);
        }

    });
    return groups;
};
function loadTeachers(){
    let teachers = [];
    $.getJSON('/teachers', function(data, status, xhr){
    }).done(function(data){
        for (let i = 0; i < data.length; i++ ) {
            teachers.push(data[i].name + ' ' + data[i].surname + ' ' + data[i].patronymic);
        }
    });
    return teachers;
};

function getPostOptions(data){
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    return options;
}
// Edit lesson
async function editLesson(parent, id){

    const response = await fetch('/lesson/' + id)
    const lesson = await response.json();
    
    let order = lesson.order
    let auditory = lesson.auditory
    let teacher = lesson.teacher
    let teacher_full = teacher.name + " " + teacher.surname + " " + teacher.patronymic; 
    let subject = lesson.subject 


    // Add tr with info field
    let info = "<tr>"
    info += "<td>"
    info += "<small>New order</small>"
    info += "</td>"
    info += "<td>"
    info += "<small>New auditory</small>"
    info += "</td>"
    info += "<td>"
    info += "<small>New teacher</small>"
    info += "</td>"
    info += "<td>"
    info += "<small>New lesson</small>"
    info += "</td>"
    info += "<td>"
    info += "<small>New lesson type</small>"
    info += "</td>"
    info += "</tr>"
    
    let row = info + "<tr class=clickable id=" + id + ">";
    // Order
    row += "<td>";
    row += "<input id='order" + id + "' type='number' class='form-control' min=1 max=5 value=" + order + ">" ;
    row += "</td>";

    // Auditory
    row += "<td>";
    row += "<input id='auditory" + id + "' type='number' class='form-control' min=1 value=" + auditory + ">" ;
    row += "</td>";

    // Teacher
    row += "<td>";
    row += "<input id='teacher" + id + "' type='text' class='form-control' value='" + teacher_full + "'>"; 
    row += "</td>";
    
    // Subject Name
    row += "<td>";
    row += "<input id='subject-title"+ id + "' type='text' class='form-control' value='" + subject.title + "'>";
    row += "</td>";

    // Subject type
    row += "<td>";
    row += "<select id='subject-type"+ id + "' class='form-control'>";
    if(subject.subj_type == 'lec'){
        row += "<option value='lec' selected>Lecture</option>";
        row += "<option value='lab'>Practise</option>";
    }else{
        row += "<option value='lab' selected>Practise</option>";
        row += "<option value='lec'>Lecture</option>";
    }
    
    row += "</select>"
    row += "<td>";

    row += "<td><button type='button' id='update-lesson" + id + "' class='btn btn-primary'>Update</button></td>";

    row += "</tr>";

    parent.replaceWith(row);

    // When updated was clicked
    $('#update-lesson' + id).on('click', async ()=>{
        // Read updated fields
        const order =  $('#order' + id).val();
        const auditory = $('#auditory' + id).val();
        const teacher = $('#teacher' + id).val().split(' ');
        const subject_title = $('#subject-title' + id).val();
        const subject_type = $('#subject-type' + id).val();

        const data = {
            'order': order,
            'auditory': auditory,
            'teacher':{
                'name': teacher[0],
                'surname': teacher[1],
                'patronymic': teacher[2]
            },
            'subject':{
                'title': subject_title,
                'subj_type': subject_type
            }
        }
        const response = await fetch('/update/lesson/' + id, getPostOptions(data));
        const resp_message = await response.json();
        if(resp_message.success === true){
            $('#flash-msg').show().text(resp_message['message']); 

            setTimeout(() => { document.location.reload(true); }, 3000);
            
        }else{
            $('#flash-msg').show().text(resp_message['message']); 
        }
        

    });
}

$(document).ready(function(){

    let groups = loadGroups();
    let teachers = loadTeachers();
    let subjects = loadSubjects();

    $('#groupname').autocomplete({
        source: groups
    });
    $('#teacher').autocomplete({
        source: teachers
    });
    // Add to all input fields
    const lessons = 5
    for(let i = 0; i < lessons; i++){
        $('#teacher' + (i+1)).autocomplete({
            source: teachers
        });
        $('#subject' + (i+1)).autocomplete({
            source: subjects
        });

    }

    $('.clickable').on("click" , async (e) =>{
        let self = $(e.target);
        let closest = self.closest("tr")
        let id = closest.attr("id");
        
        // Check if there are no buttons
        let buttons = closest.find("button")
        if (buttons.length == 0){
            let edit_btn = "<td><button type='button' id='edit-lesson" + id + "' class='btn btn-primary'>Edit</button></td>";
            let delete_btn = "<td><button type='button' id='delete-lesson" + id + "' class='btn btn-danger'>Delete</button></td>";
            closest.append(edit_btn, delete_btn);

            $("#delete-lesson" + id).on("click", async () => {
                const response = await fetch('/delete/', getPostOptions(id));
                if(response.ok){
                    
                    let lessonsInTable = closest.parent().find('tr').length
                    // Last parent
                    if (lessonsInTable == 1){
                        // Remove all day
                        closest.parents('.day').remove();
                    }else{
                        // Remove only one lesson
                        closest.remove();
                    }
                    
                }else{
                    $('#flash-msg').show().text("Cannot delete lesson!");
                }
            });

            $("#edit-lesson" + id).on("click",() =>{
                // Replace this element with form
                editLesson(closest, id);
                
            });
        }else{
            for(let i = 0;i < buttons.length; i++){
                buttons[i].closest("td").remove();
            }
        }
        
        
    });
    

    
}); 