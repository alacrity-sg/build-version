package lib

import (
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/go-git/go-git/v5"
	"github.com/go-git/go-git/v5/config"
	"github.com/go-git/go-git/v5/plumbing/object"
)

func setupRepo(branch string, t *testing.T) (string, *git.Repository, *git.Worktree, *object.Commit) {
	dir := t.TempDir()
	r, err := git.PlainInit(dir, false)
	err = r.CreateBranch(&config.Branch{Name: branch})
	w, err := r.Worktree()
	CheckIfError(err)
	fileName := filepath.Join(dir, "test.txt")
	err = os.WriteFile(fileName, []byte("test"), 0666)

	CheckIfError(err)
	_, err = w.Add("test.txt")
	CheckIfError(err)
	commit, err := w.Commit("base", &git.CommitOptions{
		Author: &object.Signature{
			Name:  "Test",
			Email: "test@test.com",
			When:  time.Now(),
		},
	})
	obj, err := r.CommitObject(commit)
	return dir, r, w, obj
}

func TestGetLatestReleaseTagSingle(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	expectedTag := "v1.0.0"
	_, err := r.CreateTag(expectedTag, commit.Hash, &git.CreateTagOptions{
		Message: expectedTag,
	})
	CheckIfError(err)
	tag, err := GetLatestReleaseTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}

func TestGetLatestReleaseTagMultiple(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	unexpectedTag := "v1.0.0"
	_, err := r.CreateTag(unexpectedTag, commit.Hash, &git.CreateTagOptions{
		Message: unexpectedTag,
	})
	CheckIfError(err)
	expectedTag := "v1.0.1"
	_, err = r.CreateTag(expectedTag, commit.Hash, &git.CreateTagOptions{
		Message: expectedTag,
	})
	CheckIfError(err)
	tag, err := GetLatestReleaseTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}

func TestGetLatestReleaseTagMultipleWithRC(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	tagOptions := &git.CreateTagOptions{
		Message: "Commit",
	}
	_, err := r.CreateTag("v1.0.0", commit.Hash, tagOptions)
	CheckIfError(err)
	expectedTag := "v1.0.1"
	_, err = r.CreateTag(expectedTag, commit.Hash, tagOptions)
	CheckIfError(err)
	_, err = r.CreateTag("v1.0.0-rc.1234", commit.Hash, tagOptions)
	CheckIfError(err)
	tag, err := GetLatestReleaseTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}

func TestGetRCTagSingle(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	tagOptions := &git.CreateTagOptions{
		Message: "Commit",
	}
	expectedTag := "v1.0.0-rc.12345as"
	_, err := r.CreateTag(expectedTag, commit.Hash, tagOptions)
	CheckIfError(err)
	tag, err := GetLatestRCTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}

func TestGetRCTagMultiple(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	tagOptions := &git.CreateTagOptions{
		Message: "Commit",
	}
	_, err := r.CreateTag("v1.0.0-rc.0000", commit.Hash, tagOptions)
	CheckIfError(err)
	expectedTag := "v1.0.0-rc.12345as"
	_, err = r.CreateTag(expectedTag, commit.Hash, tagOptions)
	CheckIfError(err)
	tag, err := GetLatestRCTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}

func TestGetRCTagMultipleWithRelease(t *testing.T) {
	dir, r, _, commit := setupRepo("main", t)
	tagOptions := &git.CreateTagOptions{
		Message: "Commit",
	}
	_, err := r.CreateTag("v1.0.0-rc.0000", commit.Hash, tagOptions)
	CheckIfError(err)
	expectedTag := "v1.0.0-rc.12345as"
	_, err = r.CreateTag(expectedTag, commit.Hash, tagOptions)
	CheckIfError(err)
	_, err = r.CreateTag("v1.0.1", commit.Hash, tagOptions)
	tag, err := GetLatestRCTag(dir)
	CheckIfError(err)
	if *tag != expectedTag[1:] {
		t.Fail()
	}
}
