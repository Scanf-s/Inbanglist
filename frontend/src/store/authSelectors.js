export const authSelectors = (state) => ({
  user: state.user,
  isAuthenticated: state.isAuthenticated,
  error: state.error,
  showModal: state.showModal,
  modalMessage: state.modalMessage,
});
