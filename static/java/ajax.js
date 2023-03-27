document.getElementById("sendMessage").addEventListener
("click", function() {
    var  messageInput = document.getElementById("messageInput");
    var messageText = messageInput.value.trim();

    if (messageText) {
        fetch("/process_message",{
            method: "POST",
            headers: {'Content-Type': 'application/json'
        },
        body: JSON.stringify({"message": messageText})
    }).
    then(response=>response.json()).
    then(data=>
    {
       
       if (data.message)
       {
         addMessageToChat('username',messageText,data.time,true);
         addMessageToChat('GPT',data.message,data.time,false);
         messageText='';
       }
    }).catch(err=>console.error(err));
    
    }

});


function addMessageToChat(sender,text,time,self)
{
    var chatArea = document.getElementById("chatArea");
    var newMessage = document.createElement("div");
    newMessage.classList.add("card","mb-3","shadow-sm","mr-3");
    newMessage.style.borderRadius="12px";
    newMessage.style.backgroundColor =self? "rgba(244,255,255)":"rgba(255,255,255)";

    var newMessageBody = document.createElement("div");
    newMessageBody.classList.add('card-body');

    var nesRow = document.createElement("div");
    nesRow.classList.add("row");

    var newHeadIconDiv = document.createElement("div");
    newHeadIconDiv.classList.add("col-1");
    var icon = document.createElement("img");
    icon.classList.add("rounded-circle");
    icon.style.width =icon.style.height ="64px";

    icon.src =self?"../static/img/情头0.png":"../static/img/情头1.png";


    var newInfoDiv = document.createElement("div");
    newInfoDiv.classList.add("col-11");

   

    var newMessageTitle= document.createElement("h5");
    newMessageTitle.classList.add("card-title");
    newMessageTitle.textContent=sender;

    var timedisplay= document.createElement("p");
    timedisplay.textContent= time;

    var segline =document.createElement("hr")
    segline.classList.add("my-auto");

    var  newMessageText = document.createElement('p');
    newMessageText.classList.add("card-text");
    newMessageText.textContent=text;

    newHeadIconDiv.appendChild(icon);
    newInfoDiv.appendChild(newMessageTitle);
    newInfoDiv.appendChild(timedisplay)

    nesRow.appendChild(newHeadIconDiv);
    nesRow.appendChild(newInfoDiv);

    newMessageBody.appendChild(nesRow);
    newMessageBody.appendChild(segline);
    newMessageBody.appendChild(newMessageText);

    newMessage.appendChild(newMessageBody);

    chatArea.insertBefore(newMessage, chatArea.querySelector(".input-group"));

}