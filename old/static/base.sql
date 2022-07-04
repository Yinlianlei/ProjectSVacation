/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2022/6/22 17:22:21                           */
/*==============================================================*/


drop table if exists administrators,userConsult,doctorinfo,kw_Sta,user_data,userinfo;


/*==============================================================*/
/* Table: administrators                                        */
/*==============================================================*/
create table administrators
(
   adm_id               int(6) not null,
   adm_psd              varchar(15),
   primary key (adm_id)
);

/*==============================================================*/
/* Table: doctorinfo                                            */
/*==============================================================*/
create table doctorinfo
(
   doctor_id            int not null,
   doctor_pnum          int(11) not null,
   doctor_name          varchar(6),
   doctor_age           int(3),
   doctor_field         varchar(20),
   doctor_level         varchar(20),
   doctor_worktime      int(2),
   online_time          int(5),
   consult_num          int(5),
   primary key (doctor_id, doctor_pnum)
);

/*==============================================================*/
/* Table: kw_Sta                                                */
/*==============================================================*/
create table kw_Sta
(
   alluser_kw           varchar(30),
   kw_num               int
);

/*==============================================================*/
/* Table: userConsult      诊断结果                                     */
/*==============================================================*/
create table userConsult
(
   user_id              int not null,
   user_pnum            int(11),
   doctor_id            int not null,
   doctor_pnum          int(11) not null,
   use_user_id          int,
   primary key (user_id, doctor_id, doctor_pnum)
);

/*==============================================================*/
/* Table: user_data            问答历史                                 */
/*==============================================================*/
create table user_data
(
   user_id              int not null,
   user_pnum            int(11),
   user_askhist         varchar(500),
   primary key (user_id)
);

/*==============================================================*/
/* Table: userinfo                                              */
/*==============================================================*/
create table userinfo
(
   user_id              int not null,
   user_pnum            int(11) not null,
   user_sex             bool,
   user_age             int(3),
   user_name            varchar(15),
   user_psd             varchar(15) not null,
   user_city            varchar(20),
   primary key (user_id, user_pnum)
);

alter table userConsult add constraint FK_Reference_3 foreign key (doctor_id, doctor_pnum)
      references doctorinfo (doctor_id, doctor_pnum) on delete restrict on update restrict;

alter table userConsult add constraint FK_Reference_5 foreign key (use_user_id)
      references user_data (user_id) on delete restrict on update restrict;

alter table userConsult add constraint FK_uers_consult_history foreign key (user_id, user_pnum)
      references userinfo (user_id, user_pnum) on delete restrict on update restrict;

alter table user_data add constraint FK_Reference_2 foreign key (user_id, user_pnum)
      references userinfo (user_id, user_pnum) on delete restrict on update restrict;

