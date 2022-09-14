document.addEventListener('DOMContentLoaded', function() {   
    window.history.pushState('The Network', 'The Network', 'http://127.0.0.1:8000/');

    document.querySelector('#followpage').addEventListener('click', () => loadpage("f",1));          
    

    document.querySelector('#allpost').addEventListener('click', () => loadpage("",1));
    loadpage("",1)
    
    const user_id = JSON.parse(document.getElementById('user_id').textContent);

    document.querySelector('#profile').addEventListener('click', ()=> loadprofilepage("p",1,user_id))
});



function updatelike(post) {
    fetch(`/post/${post.id}`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            unlikebtn = document.querySelectorAll('#lbtn'+post.id)
            for(var i of unlikebtn){i.innerHTML="unlilke"}
        } else {
            likebtn = document.querySelectorAll('#lbtn'+post.id)
            for(var i of likebtn){i.innerHTML="like"}
        }
        document.querySelectorAll('#countl'+post.id).forEach(item => {
            item.innerHTML=response.newamount;
        });
    })
}

function updatefollow(data){
    fetch(`/follow/${data.userid}`)
    .then(response => response.json())
    .then(response=>{
        if (response.followed){
            document.querySelector('#fbtn'+data.userid).innerHTML="unfollow"

        }
        else{
            document.querySelector('#fbtn'+data.userid).innerHTML="follow"

        }
        document.querySelector('#count'+data.userid).innerHTML=`following: ${response.following}&emsp;&emsp;follower: ${response.follower}`
    })
}

function loadpage(addon,page) {
    document.querySelector('#profiledetail').style.display = 'none';
    if (addon.includes("f")) {
        addon=`/f?page=${page}`;} 
    else{
        addon=`?page=${page}`;} 
    
    fetch(`/paginate${addon}`)
    .then(response => response.json())
    .then(posts => {
        document.querySelector('#inpost').innerHTML="";
        build_paginator(addon,page,posts[0].lastpage);
        for(let post of posts){
            minidiv = document.createElement('div');
            minidiv.className="card"
            minidiv.id = 'mini'+post.id
            minidiv.innerHTML= `
            <b id=${post.userid} class="nono">${post["user"]}</b>
            <h6 class="card-text">${post["datentime"]}</h6>
            <br>
            <h4 >${post["content"]}</h4>`
            document.querySelector('#inpost').append(minidiv)

            lbtn = document.createElement('button')
            lbtn.id = 'lbtn'+post.id
            lbtn.className = "btn btn-block btn-primary"
            lbtn.style = "width: 80px;"
            if (post.liked == true){
            lbtn.innerHTML = "unlike"}
            else{lbtn.innerHTML= "like"}
            lbtn.type = "button"
            minidiv.append(lbtn)
            lbtn.addEventListener('click', () => 
        updatelike(post))

            if(post.edit){
                ebtn = document.createElement('button')
                ebtn.id = 'ebtn'+post.id
                ebtn.className = "btn btn-block btn-primary"
                ebtn.style = "width: 80px;"
                ebtn.innerHTML = "edit"
                minidiv.append(ebtn)
                document.querySelector('#ebtn'+post.id).addEventListener('click',()=>editpost(post))
            }
          
                
           

            countl = document.createElement('h2')
            countl.id = 'countl'+post.id
            countl.innerHTML = post.likes
            minidiv.append(countl)
    }
    const dvar=document.querySelectorAll('.nono')
    for(const button of dvar){button.addEventListener('click',()=> loadprofilepage("p",1,button.id))}
    })
}

function build_paginator(addon,page,num_pages) {
    page_list = document.getElementById('pagination');
    page_list.innerHTML="";

    const previous = document.createElement('li');
    if(page==1){
        previous.className = "page-item disabled";    
        
    } else {
        previous.className = "page-item";    
        previous.addEventListener('click', () => loadpage(addon,page-1));
    }        
    const page_a_previous = document.createElement('a');
    page_a_previous.className="page-link";

    page_a_previous.href="#";
    page_a_previous.innerHTML="Previous";
    previous.append(page_a_previous);    
    page_list.append(previous);
    

    const next = document.createElement('li');        
    if(page==num_pages){
        next.className = "page-item disabled";    
    } else {
        next.className = "page-item";    
        next.addEventListener('click', () => loadpage(addon,page+1));
    }   
    const page_a_next = document.createElement('a');
    page_a_next.className="page-link"; 
    page_a_next.href="#";
    page_a_next.innerHTML="Next";
    next.append(page_a_next);
    page_list.append(next);    
}

function loadprofilepage(addon,page,bid) {
    profilediv = document.createElement('div');
    document.querySelector('#inpost').style.display = 'none';
    document.querySelector('#addpost').style.display = 'none';
    document.querySelector('#profiledetail').style.display = 'block';

    fetch(`/profile/${bid}`)
    .then(response=>response.json())
    .then(data=>{
        document.querySelector('#profiledetail').innerHTML=""
        profilediv.innerHTML=`
            <h1>${data.user}</h1>
            <h3 id="count${data.userid}">following: ${data.following}&emsp;&emsp;follower: ${data.follower}</h3>
            `    
        fbtn = document.createElement('button')
        fbtn.id = 'fbtn'+ data.userid
        fbtn.className = "btn btn-block btn-primary"
        if(data.status == true){
        fbtn.innerHTML = `unfollow`}
        else{fbtn.innerHTML = `follow`}

        if(data.followallow){
            profilediv.append(fbtn)
        }


        fbtn.addEventListener('click', () => 
        updatefollow(data))

        document.querySelector('#profiledetail').append(profilediv)
    }
    )
    
    

    if (addon.includes("p")) {   
        addon=`/p/${bid}?page=${page}`;} 
    fetch(`/show${addon}`)
    .then(response => response.json())
    .then(posts => {
        document.querySelector('#inprofile').innerHTML="";

        build_profilepagi(addon,page,bid,posts[0].lastpage);
        for(let post of posts){
            minidiv = document.createElement('div');
            minidiv.className="card"
            minidiv.id = 'minip'+post.id
            minidiv.innerHTML= `
            <b class="card-text">${post["user"]}</b>
            <h6 class="card-text">${post["datentime"]}</h6>
            <br>
            <h4 >${post["content"]}</h4>`
            document.querySelector('#inprofile').append(minidiv)

            lbtn = document.createElement('button')
            lbtn.id = 'lbtn'+post.id
            lbtn.className = "btn btn-block btn-primary"
            lbtn.style = "width: 80px;"
            if (post.liked == true){
            lbtn.innerHTML = "unlike"}
            else{lbtn.innerHTML= "like"}
            lbtn.type = "button"
            minidiv.append(lbtn)
            lbtn.addEventListener('click', () => 
        updatelike(post))

        if(post.edit){
            ebtn = document.createElement('button')
            ebtn.id = 'pbtn'+post.id
            ebtn.className = "btn btn-block btn-primary"
            ebtn.style = "width: 80px;"
            ebtn.innerHTML = "edit"
            minidiv.append(ebtn)
            document.querySelector('#pbtn'+post.id).addEventListener('click',()=>editpost(post))
        }

            countl = document.createElement('h2')
            countl.id = 'countl'+post.id
            countl.innerHTML = post.likes
            minidiv.append(countl)
            
    }
    })
}

function build_profilepagi(addon,page,bid,num_pages) {

    page_list = document.getElementById('pagination');
    page_list.innerHTML="";
    const previous = document.createElement('li');
    if(page==1){
        previous.className = "page-item disabled";    
    } else {
        previous.className = "page-item";    
        previous.addEventListener('click', () => loadprofilepage(addon,page-1,bid));
    }        
    const page_a_previous = document.createElement('a');
    page_a_previous.className="page-link";

    page_a_previous.href="#";
    page_a_previous.innerHTML="Previous";
    previous.append(page_a_previous);    
    page_list.append(previous);
    
    const next = document.createElement('li');        
    if(page==num_pages){
        next.className = "page-item disabled";    
    } else {
        next.className = "page-item";    
        next.addEventListener('click', () => loadprofilepage(addon,page+1,bid));
    }   
    const page_a_next = document.createElement('a');
    page_a_next.className="page-link"; 
    page_a_next.href="#";
    page_a_next.innerHTML="Next";
    next.append(page_a_next);
    page_list.append(next);
    
}

function editpost(post){

    if(document.querySelector('#ebtn'+post.id)){
    document.querySelector('#ebtn'+post.id).remove();}

    if(document.querySelector('#pbtn'+post.id)){
    document.querySelector('#pbtn'+post.id).remove();}


    editdiv = document.createElement('div');
    editdiv.id = 'editdiv'+post.id

    var newbox=document.createElement('textarea')
    newbox.id="newtext"
    newbox.className="form-control"
    var newbtn=document.createElement('button')
    newbtn.id="savepost"
    newbtn.className="form-control"
    newbtn.type="submit"
    newbtn.innerHTML="submit"
    editdiv.append(newbox)
    editdiv.append(newbtn)

    if(document.querySelector('#mini'+post.id)){
        document.querySelector('#mini'+post.id).append(editdiv)}

    if(document.querySelector('#minip'+post.id)){
    document.querySelector('#minip'+post.id).append(editdiv)}



    document.querySelector('#newtext').value= `${post['content']}`

    document.querySelector('#savepost').addEventListener('click',()=>{

    var contentload = document.querySelector('#newtext').value
    fetch(`/addpost`,{
        method:'PUT',
        headers:{"X-CSRFToken": getCookie('csrftoken') },
        body: JSON.stringify({post_id:post.id, newcontent:contentload})

    })
    .then(response=>response.text())
    .then(console.log(contentload))
    .then(res=>console.log(res))


    
    if(document.querySelector('#mini'+post.id)){
        setTimeout(function(){
            loadpage("",1),50000000
        })}

    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    if(document.querySelector('#minip'+post.id)){
        setTimeout(function(){
            loadprofilepage("p",1,user_id),50000000
        })}


    

    })

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}