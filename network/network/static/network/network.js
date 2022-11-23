function edit(id) {
    document.querySelector(`#post${id}`).style.display = 'none';
    document.querySelector(`#edit_post${id}`).style.display = 'block';
}

function edit_post(id) {
    document.querySelector(`#edit_post${id}`).style.display = 'none';
    const new_content = document.querySelector(`#edit_textarea${id}`).value;
    document.querySelector(`#content${id}`).innerHTML = new_content;
    document.querySelector(`#post${id}`).style.display = 'block';
    fetch(`/edit/${id}`, {
        method: "PUT",
        body: JSON.stringify ({
            content: new_content
        })
    })
}

function like(id) {
    if (document.querySelector(`#like_button${id}`).innerHTML == "Like") {
        const likes = parseInt(document.querySelector(`#like_count${id}`).innerHTML) + 1;
        document.querySelector(`#like_count${id}`).innerHTML = likes;
        document.querySelector(`#like_button${id}`).innerHTML = "Unlike";
        document.querySelector(`#like_button${id}`).className = "btn btn-secondary btn-sm";
        fetch(`/like/${id}`, {
            method: "PUT",
            body: JSON.stringify ({
                action: "Like"
            })
        })
        
    } else if (document.querySelector(`#like_button${id}`).innerHTML == "Unlike") {
        const likes = parseInt(document.querySelector(`#like_count${id}`).innerHTML) - 1;
        document.querySelector(`#like_count${id}`).innerHTML = likes;
        document.querySelector(`#like_button${id}`).innerHTML = "Like";
        document.querySelector(`#like_button${id}`).className = "btn btn-primary btn-sm";
        fetch(`/like/${id}`, {
            method: "PUT",
            body: JSON.stringify ({
                action: "Unlike"
            })
        })
        
    }
    
}