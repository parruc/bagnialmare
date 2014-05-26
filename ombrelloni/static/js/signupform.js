signup_form_validation = {
                message: 'Valore non valido',
                live: 'enabled',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh',
                },
                fields: {
                    neighbourhood: {
                        message: 'località non valida',
                        validators: {
                            notEmpty: {
                                message : 'scegli una località',
                            },
                            callback: {
                                message : 'scegli una località',
                                callback: function(value, validator){
                                    return value != 'nochoice'
                                }
                            }
                        }
                    },
                    bagni: {
                        message: 'bagno non valido',
                        validators: {
                            notEmpty: {
                                message : 'bagno una località',
                            },
                            callback: {
                                message : 'scegli un bagno',
                                callback: function(value, validator){
                                    return value != 'undefined'
                                }
                            }
                        }
                    },
                    name: {
                        message: 'nome non valido',
                        validators: {
                            notEmpty: {
                                message : 'il nome è richiesto e non può essere vuoto'
                            }
                        }
                    },
                    surname: {
                        message: 'cognome non valido',
                        validators: {
                            notEmpty: {
                                message : 'il cognome è richiesto e non può essere vuoto'
                            }
                        }
                    },
                    email: {
                        message: 'email non valida',
                        validators: {
                            notEmpty: {
                                message : 'l\'indirizzo mail è richiesto e non può essere vuoto'
                            },
                            emailAddress: {
                                message: 'l\'indirizzo fornito non è un email valido'
                            }
                        }
                    },
                    password1: {
                        message: 'password non valida',
                        validators: {
                            stringLength: {
                                min: 6,
                                max: 36,
                                message: 'la lunghezza della password deve essere compresa tra 6 e 36 caratteri',
                            },
                            identical: {
                                field: 'password2',
                                message: 'Password1 e Password2 devono coincidere',
                            }
                        }
                    },
                    password2: {
                        message: 'password non valida',
                        validators: {
                            stringLength: {
                                min: 6,
                                max: 36,
                                message: 'la lunghezza della password deve essere compresa tra 6 e 36 caratteri',
                            },
                            identical: {
                                field: 'password1',
                                message: 'Password1 e Password2 devono coincidere',
                            }
                        }
                    },
                    tos: {
                        message: 'tos non valido',
                        validators: {
                            choice: {
                                min: 1,
                                message : 'devi accettare i termini del servizio per proseguire'
                            }
                        }
                    },
                    privacy: {
                        message: 'privacy non valido',
                        validators: {
                            choice: {
                                min: 1,
                                message : 'devi accettare i termini della privacy per proseguire'
                            }
                        }
                    },
                }
            };
