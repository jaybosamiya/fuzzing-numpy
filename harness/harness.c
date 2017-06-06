#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <sys/mman.h>
#include <errno.h>
#include <signal.h>
#include <time.h>

#define DEBUG_LEVEL DEBUG_3
#define TEST_CASE_SIZE (1<<20)

typedef enum {FATAL, VERBOSE, DEBUG, DEBUG_2, DEBUG_3} debug_t;
const char* debug_messages[] = {"!! FATAL !!","+",">", ">>", ">>>"};

/* Externally accessible functions */
void register_testcase(const char *t);

/* Internals for the .so */
static char * current_test_case;
static void init() __attribute__((constructor)); // force running when
						 // .so is loaded
static void debug(debug_t level, const char * fmt, ...);
static void fatal_err(const char * message);
static void sighandler(int sig);

void init() {
  /* Set up using mmap, so that crashing Python doesn't affect us */
  current_test_case = mmap(NULL,
			   TEST_CASE_SIZE,
			   PROT_READ | PROT_WRITE,
			   MAP_PRIVATE | MAP_ANONYMOUS,
			   -1, 0);

  if ( current_test_case == MAP_FAILED )
    fatal_err("Failed creating mmap'd region.");
  
  debug(DEBUG, "Created mmap'd region at %p", current_test_case);

  if ( signal(SIGSEGV, sighandler) == SIG_ERR )
    fatal_err("Failed setting up sighandler for SIGSEGV");
  if ( signal(SIGABRT, sighandler) == SIG_ERR )
    fatal_err("Failed setting up sighandler for SIGABRT");

  debug(DEBUG, "Set up signal handlers");

  debug(DEBUG_3, "Current PID = %u", getpid());
}

void register_testcase(const char *t) {
  strcpy(current_test_case, t);
}

void sighandler(int sig) {
  debug(VERBOSE, "Received signal %d.", sig);
  char filename[256];
  sprintf(filename,
	  "crashes/crash_%d_%lu_%u.dump",
	  sig,
	  time(NULL), // Add uniqueness to filename
	  getpid()); // Further uniqueness
  int fd = open(filename, O_WRONLY | O_CREAT,
		S_IRWXU | S_IRWXG | S_IRWXO);
  if ( fd == -1 )
    fatal_err("Could not open file for dumping");
  if ( write(fd, current_test_case, strlen(current_test_case)) == -1 )
    fatal_err("Could not write to dump file");
  if ( close(fd) == -1 )
    fatal_err("Could not close dump file");

  debug(VERBOSE, "Finished dumping test case :) Exiting cleanly.");
  exit(0);
}

void debug(debug_t level, const char * fmt, ...) {
  if ( level > DEBUG_LEVEL )
    return;

  fprintf(stderr, "[%s] ", debug_messages[level]);

  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);
  va_end(ap);

  fprintf(stderr, "\n");
}

void fatal_err(const char * message) {
  debug(FATAL, "%s Exiting.", message);
  debug(FATAL, "Error: %s", strerror(errno));
  exit(1);
}
