(function () {
  const editButtons = document.getElementsByClassName("btn-edit");
  const commentText = document.getElementById("id_body");
  const commentForm = document.getElementById("commentForm");
  const submitButton = document.getElementById("submitButton");

  const deleteModal = new bootstrap.Modal(
    document.getElementById("deleteModal")
  );
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteForm = document.getElementById("deleteCommentForm");

  /**
   * Initializes edit functionality for the provided edit buttons.
   *
   * For each button in the `editButtons` collection:
   * - Retrieves the associated comment's ID upon click.
   * - Fetches the content of the corresponding comment.
   * - Populates the `commentText` input/textarea with the comment's content for editing.
   * - Updates the submit button's text to "Update".
   * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
   */
  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("comment_id");
      let slug = e.target.getAttribute("data-slug"); // Fetch the event slug
      let commentContent = document.getElementById(
        `comment${commentId}`
      ).innerText;

      commentForm.setAttribute(
        "action",
        `/event/${slug}/edit_comment/${commentId}/`
      );
      commentText.value = commentContent;
      submitButton.innerText = "Update"; // Update button text
    });
  }

  /**
   * Initializes deletion functionality for the provided delete buttons.
   *
   * For each button in the `deleteButtons` collection:
   * - Retrieves the associated comment's ID upon click.
   * - Updates the `deleteConfirm` link's href to point to the
   * deletion endpoint for the specific comment.
   * - Displays a confirmation modal (`deleteModal`) to prompt
   * the user for confirmation before deletion.
   */
  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("comment_id");
      let slug = e.target.getAttribute("data-slug");

      // Update the form action to the delete comment URL
      deleteForm.setAttribute(
        "action",
        `/event/${slug}/delete_comment/${commentId}/`
      );

      // Show the delete modal
      deleteModal.show();
    });
  }
})();
