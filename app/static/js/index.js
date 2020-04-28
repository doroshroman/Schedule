$(document).ready(function(){

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
    
    
}); 