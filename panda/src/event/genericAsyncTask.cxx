// Filename: genericAsyncTask.cxx
// Created by:  drose (03Oct08)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#include "genericAsyncTask.h"
#include "pnotify.h"

TypeHandle GenericAsyncTask::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
GenericAsyncTask::
GenericAsyncTask(const string &name) :
  AsyncTask(name)
{
  _function = NULL;
  _upon_birth = NULL;
  _upon_death = NULL;
  _user_data = NULL;
}

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
GenericAsyncTask::
GenericAsyncTask(const string &name, GenericAsyncTask::TaskFunc *function, void *user_data) :
  AsyncTask(name),
  _function(function),
  _user_data(user_data)
{
  _upon_birth = NULL;
  _upon_death = NULL;
}

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::is_runnable
//       Access: Protected, Virtual
//  Description: Override this function to return true if the task can
//               be successfully executed, false if it cannot.  Mainly
//               intended as a sanity check when attempting to add the
//               task to a task manager.
//
//               This function is called with the lock held.
////////////////////////////////////////////////////////////////////
bool GenericAsyncTask::
is_runnable() {
  return _function != NULL;
}

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::do_task
//       Access: Protected, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
AsyncTask::DoneStatus GenericAsyncTask::
do_task() {
  nassertr(_function != NULL, DS_abort);
  return (*_function)(this, _user_data);
}

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::upon_birth
//       Access: Protected, Virtual
//  Description: Override this function to do something useful when the
//               task has been added to the active queue.
//
//               This function is called with the lock held.  You may
//               temporarily release if it necessary, but be sure to
//               return with it held.
////////////////////////////////////////////////////////////////////
void GenericAsyncTask::
upon_birth() {
  AsyncTask::upon_birth();

  if (_upon_birth != NULL) {
    release_lock();
    (*_upon_birth)(this, _user_data);
    grab_lock();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: GenericAsyncTask::upon_death
//       Access: Protected, Virtual
//  Description: Override this function to do something useful when the
//               task has been removed from the active queue.  The
//               parameter clean_exit is true if the task has been
//               removed because it exited normally (returning
//               DS_done), or false if it was removed for some other
//               reason (e.g. AsyncTaskManager::remove()).
//
//               The normal behavior is to throw the done_event only
//               if clean_exit is true.
//
//               This function is called with the lock held.  You may
//               temporarily release if it necessary, but be sure to
//               return with it held.
////////////////////////////////////////////////////////////////////
void GenericAsyncTask::
upon_death(bool clean_exit) {
  AsyncTask::upon_death(clean_exit);

  if (_upon_death != NULL) {
    release_lock();
    (*_upon_death)(this, clean_exit, _user_data);
    grab_lock();
  }
}
