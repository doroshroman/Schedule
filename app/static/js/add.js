$(document).ready(function(){
    let groupName;
    let date;
    let maxPairs = 5;
    for (let i=0; i<maxPairs; i++){
        let subject =`<tr> 
        <td>${i + 1}</td>
        <td><input id='auditory${i + 1}' type='text' class='form-control'  ></td>
        <td><input id='teacher${i + 1}' type='text' class='form-control'</td>
        <td><input id='subject${i + 1}' type='text' class='form-control'</td>
        <td><select id='subject-type${i + 1}' class='form-control'>
        <option value='lec' selected>Lecture</option>
        <option value='lab'>Practice</option></select>
        </td>
        </tr>
        `
        $('#adding-table >tbody').append(subject);
    }
    $('#add-day').click(async (e) =>{
            e.preventDefault();
            groupName = $('#groupname').val().trim();
            date = $('#date').val().trim();
        for (let i=0;i<maxPairs; i++){
            let order = i+1;
            let auditory = $('#auditory'+ (i+1)).val().trim();
            let teacher = $('#teacher'+ (i+1)).val().split(' ');
            let subject = $('#subject'+ (i+1)).val().trim();
            let subjectType = $('#subject-type'+ (i+1)).val();

            const data = {
                'date' : date,
                'groupname' : groupName,
                'order': order,
                'auditory': auditory,
                'teacher':{
                    'name': teacher[0],
                    'surname': teacher[1],
                    'patronymic': teacher[2]
                },
                'subject':{
                    'title': subject,
                    'subj_type': subjectType
                }
            }
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
            const response = await fetch('/add_schedule', options)
            const content_type = response.headers.get('Content-Type');
            if (content_type.search('json') != -1){
            const data = await response.json();
                if (data.success == true){
                    $('#copyform').show()
                }
        }
    }
    })

    $('#copy').click(async (e) =>{
        e.preventDefault();
        groupName = $('#groupname').val().trim();
        date = $('#date').val().trim();
        let dateFrom = $('#date-from').val();
        let dateTo = $('#date-to').val();
        let weekType =$('#week').val();
        let dayType =$('#day-of-week').val();
        const copyData = {
            'groupname': groupName,
            'date': date,
            'date_from': dateFrom,
            'date_to': dateTo,
            'week_type': weekType,
            'day_type': dayType
        }
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(copyData)
        }
        const response = await fetch('/copy_schedule', options)

    })
})