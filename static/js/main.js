var myVar;
function myFunction() {
  myVar = setTimeout(showPage, 1000);
}
function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}


function setreact(json){
         document.getElementById('like').innerText=json.res[0].likes
         document.getElementById('dislike').innerText=json.res[0].dislikes
}
function setcomment(comment){
    comments_html=document.getElementById('comments')
    new_comment=`
    <li>${comment}</li>`
    comments_html.innerHTML+=new_comment
    console.log(comments_html)
    document.getElementById('comment').value=''
}

function reaction(id,react){
    const url=`/reaction/${id}/${react}`
    console.log(url)
    const request=new Request(
        url,
        {
        method:'GET',
        headers:{'X-CSRFToken':csrftoken}
        }
    );
    fetch(request)
    .then(response => response.json())
    .then(json => setreact(json))
    };
function send_comment(id){
    text=document.getElementById('comment').value
    url=`/comment/${id}`
    request= new Request(
     url,
        {
        method:'POST',
        headers:{'X-CSRFToken':csrftoken},
        body:JSON.stringify({
        'comment':text
        })
        }
     )
     fetch(request)
        .then(response =>{
        if (response.status==201)
            setcomment(text)

    })
//    .then((data) => {
//     console.log(data);
//    });
//    }
}