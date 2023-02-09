document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = sendmail;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sendmail(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value
  const subject = document.querySelector('#compose-subject').value
  const body = document.querySelector('#compose-body').value

  fetch("/emails",
    {
      method: "post",
      body: JSON.stringify(
        {
          recipients: recipients,
          subject: subject,
          body: body
        })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    })
    localStorage.clear();
    setTimeout(()=>{ load_mailbox('sent');}, 100)
    return false;
}



function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    if (emails.length == 0){
      document.querySelector('#emails-view').innerHTML = `<p>No email.</p>`;
    }


    for (let email of emails) {      
      const email_div = document.createElement('div');
      email_div.className ="card"

      if (email['read']==false){
      email_div.style.backgroundColor = "lightgray";}
      else{email_div.style.backgroundColor = "white"}




      email_div.style.display = "flex";


      if (mailbox === "inbox"|| mailbox == "archive") {
        
        email_div.innerHTML = `
        <div style=width:300px>${email["sender"]}</div>
        <div style=margin-left:10px>${email["subject"]}</div>
        <div style="margin-left:auto">${email["timestamp"]}</div>
        
      `;
      }

      else
      { 
        email_div.innerHTML = `
        <div style=width:300px>${email["recipients"]}</div>
        <div style=margin-left:10px>${email["subject"]}</div>
        <div style="margin-left:auto">${email["timestamp"]}</div>
      `;
      }

      email_div.addEventListener('click', () => load_email(email));
      email_div.addEventListener('click', () => reademail(email.id));

      document.querySelector('#emails-view').append(email_div);
    


      const btn = document.createElement('button');
      btn.id = 'archivebtn'

      if(email.archived==false){
        btn.innerHTML = "archive it";
        btn.className = "btn btn-success";}
      else{
        btn.innerHTML = "unarchive"
        btn.className = "btn btn-danger";}
      
      if (mailbox === "inbox" || mailbox ==="archive") {
      email_div.append(btn);}
      btn.addEventListener('click', () => 
        archivemail(email.id, email.archived)
      );
      


    };
  })
}

function archivemail(email_id, archived)
{
  fetch(`/emails/${email_id}`,{
    method :'PUT',
    body : JSON.stringify({
      archived : !archived
    })
  })
  load_mailbox('inbox');
  window.location.reload()
}

function replymail(email)
{
  compose_email();
  document.querySelector('#compose-recipients').value = email['sender'];
  let subject = "Re: " + email['subject'];
  document.querySelector('#compose-subject').value = subject;
  
  document.querySelector(
    '#compose-body').value = `${email['timestamp']}, 
${email['sender']} wrote: ${email['body']}`;

}

function reademail(email_id)
{
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  
}



function load_email(email) {
  //keeping only the email-view and hiding the rest
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  email_view = document.querySelector('#email-view');
  email_view.style.display = 'block';
  
  // view mail
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {

    email_view.innerHTML = `
      <div>${email.sender}</span><div>
      <div>${email.recipients}<div>
      <div>${email.subject}<div>
      <div>${email.timestamp}<div>
            <hr>
      <div>${email.body}</div>
    `;
    const reply = document.createElement('button');
    reply.innerHTML = "reply";
    reply.id = "replybtn";
    reply.className="btn btn-primary";
    reply.addEventListener('click', () => 
        replymail(email)
      );
    email_view.append(reply);

    const btn = document.createElement('button');
    btn.id = 'archivebtn'
    if (email.archived==false){
    btn.innerHTML = "archive it";
    btn.className = "btn btn-success";}
    else{
    btn.innerHTML = "unarchive";
    btn.className = "btn btn-danger"}
    email_view.append(btn);

    btn.addEventListener('click', () => 
      archivemail(email.id, email.archived)
    );


    if (document.querySelector('#users_email').innerHTML === email.sender) {
      document.querySelector('#archivebtn').remove()
    }
    if (document.querySelector('#users_email').innerHTML === email.sender) {
      document.querySelector('#replybtn').remove()
    }


  })
 
}




