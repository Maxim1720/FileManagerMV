#!/bin/sh
# Copyright 2000-2021 JetBrains s.r.o. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

# ---------------------------------------------------------------------
# PyCharm startup script.
# ---------------------------------------------------------------------

message()
{
  TITLE="Cannot start PyCharm"
  if [ -n "$(command -v zenity)" ]; then
    zenity --error --title="$TITLE" --text="$1" --no-wrap
  elif [ -n "$(command -v kdialog)" ]; then
    kdialog --error "$1" --title "$TITLE"
  elif [ -n "$(command -v notify-send)" ]; then
    notify-send "ERROR: $TITLE" "$1"
  elif [ -n "$(command -v xmessage)" ]; then
    xmessage -center "ERROR: $TITLE: $1"
  else
    printf "ERROR: %s\n%s\n" "$TITLE" "$1"
  fi
}

if [ -z "$(command -v uname)" ] || [ -z "$(command -v realpath)" ] || [ -z "$(command -v dirname)" ] || [ -z "$(command -v cat)" ] || \
   [ -z "$(command -v egrep)" ]; then
  TOOLS_MSG="Required tools are missing:"
  for tool in uname realpath egrep dirname cat ; do
     test -z "$(command -v $tool)" && TOOLS_MSG="$TOOLS_MSG $tool"
  done
  message "$TOOLS_MSG (SHELL=$SHELL PATH=$PATH)"
  exit 1
fi

# shellcheck disable=SC2034
GREP_OPTIONS=''
OS_TYPE=$(uname -s)
OS_ARCH=$(uname -m)

# ---------------------------------------------------------------------
# Ensure $IDE_HOME points to the directory where the IDE is installed.
# ---------------------------------------------------------------------
IDE_BIN_HOME=$(dirname "$(realpath "$0")")
IDE_HOME=$(dirname "${IDE_BIN_HOME}")
CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"
PRODUCT_VENDOR="JetBrains"
PATHS_SELECTOR="PyCharmCE2021.1"

# ---------------------------------------------------------------------
# Locate a JRE installation directory command -v will be used to run the IDE.
# Try (in order): $PYCHARM_JDK, .../pycharm.jdk, .../jbr[-x86], $JDK_HOME, $JAVA_HOME, "java" in $PATH.
# ---------------------------------------------------------------------
# shellcheck disable=SC2154
if [ -n "$PYCHARM_JDK" ] && [ -x "$PYCHARM_JDK/bin/java" ]; then
  JRE="$PYCHARM_JDK"
fi

BITS=""
if [ -z "$JRE" ] && [ -s "${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/pycharm.jdk" ]; then
  USER_JRE=$(cat "${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/pycharm.jdk")
  if [ -x "$USER_JRE/bin/java" ]; then
    JRE="$USER_JRE"
  fi
fi

if [ -z "$JRE" ] && [ "$OS_TYPE" = "Linux" ]; then
  if [ "$OS_ARCH" = "x86_64" ] && [ -d "$IDE_HOME/jbr" ]; then
    JRE="$IDE_HOME/jbr"
  elif [ -d "$IDE_HOME/jbr-x86" ] && "$IDE_HOME/jbr-x86/bin/java" -version > /dev/null 2>&1 ; then
    JRE="$IDE_HOME/jbr-x86"
  fi
fi

# shellcheck disable=SC2153
if [ -z "$JRE" ]; then
  if [ -n "$JDK_HOME" ] && [ -x "$JDK_HOME/bin/java" ]; then
    JRE="$JDK_HOME"
  elif [ -n "$JAVA_HOME" ] && [ -x "$JAVA_HOME/bin/java" ]; then
    JRE="$JAVA_HOME"
  fi
fi

if [ -z "$JRE" ]; then
  JAVA_BIN=$(command -v java)
else
  JAVA_BIN="$JRE/bin/java"
fi

if [ -z "$JAVA_BIN" ] || [ ! -x "$JAVA_BIN" ]; then
  X86_JRE_URL=""
  # shellcheck disable=SC2166
  if [ -n "$X86_JRE_URL" ] && [ ! -d "$IDE_HOME/jbr-x86" ] && [ "$OS_ARCH" = "i386" -o "$OS_ARCH" = "i686" ]; then
    message "To run PyCharm on a 32-bit system, please download 32-bit Java runtime from \"$X86_JRE_URL\" and unpack it into \"jbr-x86\" directory."
  else
    message "No JRE found. Please make sure \$PYCHARM_JDK, \$JDK_HOME, or \$JAVA_HOME point to valid JRE installation."
  fi
  exit 1
fi

if [ -n "$JRE" ] && [ -r "$JRE/release" ]; then
  egrep -q -E -e "OS_ARCH=\"(x86_64|amd64)\"" "$JRE/release" && BITS="64" || BITS=""
else
  test "${OS_ARCH}" = "x86_64" && BITS="64" || BITS=""
fi

# ---------------------------------------------------------------------
# Collect JVM options and IDE properties.
# ---------------------------------------------------------------------
# shellcheck disable=SC2154
if [ -n "$PYCHARM_PROPERTIES" ]; then
  IDE_PROPERTIES_PROPERTY="-Didea.properties.file=$PYCHARM_PROPERTIES"
fi

VM_OPTIONS_FILE=""
USER_VM_OPTIONS_FILE=""
# shellcheck disable=SC2154
if [ -n "$PYCHARM_VM_OPTIONS" ] && [ -r "$PYCHARM_VM_OPTIONS" ]; then
  # 1. $<IDE_NAME>_VM_OPTIONS
  VM_OPTIONS_FILE="$PYCHARM_VM_OPTIONS"
elif [ -r "${IDE_HOME}.vmoptions" ]; then
  # 2. <IDE_HOME>.vmoptions || <IDE_HOME>/bin/<bin_name>.vmoptions + <IDE_HOME>.vmoptions (Toolbox)
  VM_OPTIONS_FILE="${IDE_HOME}.vmoptions"
  if ! egrep -q -e "^-ea$" "${IDE_HOME}.vmoptions" && [ -r "${IDE_BIN_HOME}/pycharm${BITS}.vmoptions" ]; then
    VM_OPTIONS_FILE="${IDE_BIN_HOME}/pycharm${BITS}.vmoptions"
    USER_VM_OPTIONS_FILE="${IDE_HOME}.vmoptions"
  fi
elif [ -r "${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/pycharm${BITS}.vmoptions" ]; then
  # 3. <config_directory>/<bin_name>.vmoptions
  VM_OPTIONS_FILE="${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/pycharm${BITS}.vmoptions"
else
  # 4. <IDE_HOME>/bin/[<os>/]<bin_name>.vmoptions [+ <config_directory>/user.vmoptions]
  if [ -r "${IDE_BIN_HOME}/pycharm${BITS}.vmoptions" ]; then
    VM_OPTIONS_FILE="${IDE_BIN_HOME}/pycharm${BITS}.vmoptions"
  else
    test "${OS_TYPE}" = "Darwin" && OS_SPECIFIC="mac" || OS_SPECIFIC="linux"
    if [ -r "${IDE_BIN_HOME}/${OS_SPECIFIC}/pycharm${BITS}.vmoptions" ]; then
      VM_OPTIONS_FILE="${IDE_BIN_HOME}/${OS_SPECIFIC}/pycharm${BITS}.vmoptions"
    fi
  fi
  if [ -r "${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/user.vmoptions" ]; then
    if [ -n "$VM_OPTIONS_FILE" ]; then
      VM_OPTIONS="${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/user.vmoptions"
    else
      USER_VM_OPTIONS_FILE="${CONFIG_HOME}/${PRODUCT_VENDOR}/${PATHS_SELECTOR}/user.vmoptions"
    fi
  fi
fi

VM_OPTIONS=""
if [ -n "$VM_OPTIONS_FILE" ]; then
  VM_OPTIONS=$(cat "$VM_OPTIONS_FILE" "$USER_VM_OPTIONS_FILE" 2> /dev/null | egrep -v -e "^#.*")
else
  message "Cannot find VM options file"
fi

CLASSPATH="$IDE_HOME/lib/bootstrap.jar"
CLASSPATH="$CLASSPATH:$IDE_HOME/lib/util.jar"
CLASSPATH="$CLASSPATH:$IDE_HOME/lib/jdom.jar"
CLASSPATH="$CLASSPATH:$IDE_HOME/lib/log4j.jar"
CLASSPATH="$CLASSPATH:$IDE_HOME/lib/jna.jar"
# shellcheck disable=SC2154
if [ -n "$PYCHARM_CLASSPATH" ]; then
  CLASSPATH="$CLASSPATH:$PYCHARM_CLASSPATH"
fi

# ---------------------------------------------------------------------
# Run the IDE.
# ---------------------------------------------------------------------
IFS="$(printf '\n\t')"
# shellcheck disable=SC2086
"$JAVA_BIN" \
  -classpath "$CLASSPATH" \
  ${VM_OPTIONS} \
  "-XX:ErrorFile=$HOME/java_error_in_pycharm_%p.log" \
  "-XX:HeapDumpPath=$HOME/java_error_in_pycharm_.hprof" \
  "-Didea.vendor.name=${PRODUCT_VENDOR}" \
  "-Didea.paths.selector=${PATHS_SELECTOR}" \
  "-Djb.vmOptionsFile=${USER_VM_OPTIONS_FILE:-${VM_OPTIONS_FILE}}" \
  ${IDE_PROPERTIES_PROPERTY} \
  -Didea.platform.prefix=PyCharmCore \
  com.intellij.idea.Main \
  "$@"
