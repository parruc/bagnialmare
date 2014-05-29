edit_form_validation = {
                message: 'Valore non valido',
                live: 'enabled',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh',
                },
                fields: {
                    name: {
                        message: 'nome non valido',
                        validators: {
                            stringLength: {
                                min: 1,
                                max: 150,
                                message: 'la lunghezza del nome deve essere compresa tra 1 e 150 caratteri',
                            },
                        }
                    },
                    number: {
                        message: 'numero non valido',
                        validators: {
                            stringLength: {
                                min: 1,
                                max: 20,
                                message: 'la lunghezza del nome deve essere compresa tra 1 e 20 caratteri',
                            },
                        }
                    },
                    address: {
                        message: 'indirizzo non valido',
                        validators: {
                            stringLength: {
                                min: 1,
                                max: 100,
                                message: 'la lunghezza dell\'indirizzo deve essere compresa tra 1 e 100 caratteri',
                            },
                        }
                    },
                    site: {
                        message: 'link non valido',
                        validators: {
                            uri: {
                                message: 'link non valido',
                            },
                        }
                    },
                    mail: {
                        message: 'email non valida',
                        validators: {
                            emailAddress: {
                                message: 'l\'indirizzo fornito non è un email valido'
                            }
                        }
                    },
                    description_en: {
                        message: 'descrizione non valida',
                        //selector: 'textarea[id^="id_description"]',
                        validators: {
                            stringLength: {
                                max: 350,
                                message: 'Puoi inserire un massimo di 350 caratteri',
                            },
                        }
                    },
                    description_it: {
                        message: 'descrizione non valida',
                        //selector: 'textarea[id^="id_description"]',
                        validators: {
                            stringLength: {
                                max: 350,
                                message: 'Puoi inserire un massimo di 350 caratteri',
                            },
                        }
                    },
            }
};
