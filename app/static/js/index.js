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

$(document).ready(function(){

    let groups = loadGroups();
    let teachers = loadTeachers();
    let subjects = loadSubjects();

    $('#groupname').autocomplete({
        source: groups
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

    $('.clickable').on("click" , (e) =>{
        let self = $(e.target);
        let closest = self.closest("tr")
        let id = closest.attr("id");
        
        // Check if there are no buttons
        if (closest.find("button").length == 0){
            let edit_btn = "<td><button type='button' id='edit-lesson' class='btn btn-primary'>Edit</button></td>";
            let delete_btn = "<td><button type='button' id='delete-lesson' class='btn btn-danger'>Delete</button></td>";
            closest.append(edit_btn, delete_btn);
            
            $("#delete-lesson").on("click",async () => {
                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(id)
                }
                const response = await fetch('/delete', options);
                if(response.ok){
                    closest.remove(); 
                }
            });
        }
        
        
    });
    
    


    
}); 